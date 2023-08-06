import hashlib
import json
import yaml
import os
import sys
import shutil
import subprocess
import tempfile
import logging
import posixpath
import docker
import platform
from os.path import expanduser
from os.path import sep as separator
import requests
from requests.exceptions import HTTPError
import boto3
from urllib.parse import urlparse
import configparser
import base64

from mlflow.projects.backend.abstract_backend import AbstractBackend
import mlflow.tracking as tracking
from mlflow.entities import RunStatus
from mlflow.projects.submitted_run import SubmittedRun
from mlflow.projects.utils import (
    fetch_and_validate_project,
    get_or_create_run,
    load_project,
    get_entry_point_command,
    get_run_env_vars
)
import mlflow.projects
import mlflow.projects.docker
from mlflow.utils import process, file_utils
from mlflow.utils.mlflow_tags import MLFLOW_PROJECT_ENV, MLFLOW_PROJECT_BACKEND
import mlflow.projects.kubernetes
from mlflow.projects.kubernetes import KubernetesSubmittedRun, _get_run_command, _load_kube_context
import kubernetes
from kubernetes.config.config_exception import ConfigException
from infinstor_mlflow_plugin.cognito_auth_rest_store import CognitoAuthenticatedRestStore
from infinstor_mlflow_plugin import tokenfile

_logger = logging.getLogger(__name__)

verbose = True

'''
For running in k8s, invoke as 'mlflow run . -b infinstor-backend --backend-config kubernetes_config.json'
kubernetes_config.json contains:
{
    "kube-context": "minikube",
    "kube-job-template-path": "kubernetes_job_template.yaml",
    "repository-uri": "public.ecr.aws/l9n7x1v8/mlflow-projects-demo/full-image"
}
repository-uri is the uri where the full container img, i.e. docker env for MLproject plus MLproject files will be pushed
docker env for the MLproject is pushed to by: cd to the MLproject and running
$ docker build .
$ docker tag <image_id_printed_from_prev_cmd> public.ecr.aws/l9n7x1v8/mlflow-projects-demo/base-image
$ docker push public.ecr.aws/l9n7x1v8/mlflow-projects-demo/base-image

kubernetes_job_template contains:
apiVersion: batch/v1
kind: Job
metadata:
  name: "{replaced with MLflow Project name}"
  namespace: default
spec:
  ttlSecondsAfterFinished: 100
  backoffLimit: 0
  template:
    spec:
      containers:
      - name: "{replaced with MLflow Project name}"
        image: "{replaced with URI of Docker image created during Project execution}"
        command: ["{replaced with MLflow Project entry point command}"]
        #env: ["{appended with MLFLOW_TRACKING_URI, MLFLOW_RUN_ID and MLFLOW_EXPERIMENT_ID}"]
        env: []
        resources:
          limits:
            memory: 512Mi
          requests:
            memory: 256Mi
      restartPolicy: Never
'''

class InfinStorSubmittedRun(SubmittedRun):
    """
    A run that just does nothing
    """

    def __init__(self, run_id):
        self._run_id = run_id

    def wait(self):
        return True

    def get_status(self):
        return RunStatus.FINISHED

    def cancel(self):
        pass

    @property
    def run_id(self):
        return self._run_id



def upload_objects(run_id, bucket_name, path_in_bucket, local_path):
    if (path_in_bucket[0] == '/'):
        path_in_bucket = path_in_bucket[1:]
    if (verbose):
        print('upload_objects: Entered. bucket=' + bucket_name
                + ', path_in_bucket=' + path_in_bucket + ', local_path=' + local_path)
    try:
        for path, subdirs, files in os.walk(local_path):
            path = path.replace("\\","/")
            directory_name = path.replace(local_path, "")
            for onefile in files:
                src_path = os.path.join(path, onefile)
                if (path_in_bucket.endswith('/')):
                    path_in_bucket = path_in_bucket[:-1]
                if (directory_name.startswith('/')):
                    directory_name = directory_name[1:]
                if (len(directory_name) > 0):
                    dst_path = path_in_bucket + '/' + directory_name
                else:
                    dst_path = path_in_bucket
                    dst_path = dst_path.rstrip('\n')
                if (verbose):
                    print('upload_objects: Uploading ' + src_path + ' to ' + dst_path)
                tracking.MlflowClient().log_artifact(run_id, src_path, dst_path)
    except Exception as err:
        print(err)

def extract_creds():
    home = expanduser("~")
    if (verbose):
        print("User's Home Directory is " + home);
    config = configparser.ConfigParser()
    credsfile = home + separator + ".aws" + separator + "credentials"
    config.read(credsfile)
    for section in config.sections():
        if (section == 'infinstor'):
            dct = dict(config[section])
            return dct['aws_access_key_id'], dct['aws_secret_access_key']
    return None, None

class PluginInfinStorProjectBackend(AbstractBackend):
    def run(self, project_uri, entry_point, params,
            version, backend_config, tracking_store_uri, experiment_id):

        if (verbose):
            print("PluginInfinStorProjectBackend: Entered. project_uri=" + str(project_uri)\
                + ", entry_point=" + str(entry_point)\
                + ", params=" + str(params)\
                + ", version=" + str(version)\
                + ", backend_config=" + str(backend_config)\
                + ", experiment_id=" + str(experiment_id)\
                + ", tracking_store_uri=" + str(tracking_store_uri))

        work_dir = fetch_and_validate_project(project_uri, version, entry_point, params)
        active_run = get_or_create_run(None, project_uri, experiment_id, work_dir, version,
                                       entry_point, params)
        if (verbose):
            print('active_run=' + str(active_run))
            print('active_run.info=' + str(active_run.info))

        artifact_uri = active_run.info.artifact_uri
        run_id = active_run.info.run_id

        print('run_id=' + str(run_id))

        tags = active_run.data.tags
        if (tags['mlflow.source.type'] != 'PROJECT'):
            raise ValueError('mlflow.source_type must be PROJECT. Instead it is '\
                    + tags['mlflow.source.type'])

        if ('parent_run_id' in backend_config):
            parent_run_id = backend_config['parent_run_id']
            tracking.MlflowClient().set_tag(active_run.info.run_id,
                    'mlflow.parentRunId', parent_run_id)

        pdst = urlparse(artifact_uri)
        bucket_name = pdst.netloc
        if (pdst.path[0] == '/'):
            path_in_bucket = pdst.path[1:]
        else:
            path_in_bucket = pdst.path

        localdir = tags['mlflow.source.name']
        if ('mlflow.source.git.repoURL' in tags or
                'mlflow.gitRepoURL' in tags or
                'mlflow.source.git.commit' in tags):
            pl = urlparse(localdir)
            if (not pl.scheme == 'file'):
                raise ValueError('Cannot deal with scheme ' + pl.scheme + ' in source path')
            localdir = pl.path + separator + pl.fragment


        project = load_project(work_dir)
        tracking.MlflowClient().set_tag(active_run.info.run_id, MLFLOW_PROJECT_BACKEND, "infinstor")

        kube_job_template_path = backend_config.get('kube-job-template-path')
        if kube_job_template_path:
            return self.run_kube(project_uri, entry_point, params, version,
                    backend_config, tracking_store_uri, experiment_id, project, active_run, work_dir)

        instance_type = backend_config['instance_type']
        if (verbose):
            print('running in the cloud in an instance of type: ' + instance_type)
        upload_objects(run_id, bucket_name, '.infinstor/project_files', localdir)
        body = dict()
        body['project_files_bucket'] = bucket_name
        body['project_files_path_in_bucket'] = path_in_bucket
        body['params'] = params
        body['run_id'] = run_id
        body['experiment_id'] = str(experiment_id)
        body['instance_type'] = instance_type
        if ('parent_run_id' in backend_config):
            body['parent_run_id'] = backend_config['parent_run_id']
        if ('last_in_chain_of_xforms' in backend_config):
            body['last_in_chain_of_xforms'] = backend_config['last_in_chain_of_xforms']
        body['dot_infinstor_contents'] = open(tokenfile.get_token_file_name(), "r").read()

        if project.docker_env:
            body['docker_image'] = project.docker_env.get("image")

        key, secret = extract_creds()
        if (key != None):
            body['aws_access_key_id'] = key
            body['aws_secret_access_key'] = secret

        cog = CognitoAuthenticatedRestStore()
        headers = {
                'Content-Type': 'application/x-amz-json-1.1',
                'Authorization' : 'Bearer ' + cog.get_token_string()
                }
        url = 'https://' + cog.get_service() + '/api/2.0/mlflow/projects/run-project'

        try:
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        else:
            return InfinStorSubmittedRun(active_run.info.run_id)

    def run_kube(self, project_uri, entry_point, params,
            version, backend_config, tracking_store_uri, experiment_id, project, active_run, work_dir):
        kube_context = backend_config.get('kube-context')
        repository_uri = backend_config.get('repository-uri')
        kube_job_template_path = backend_config.get('kube-job-template-path')
        if (verbose):
            print("PluginInfinStorProjectBackend: run_kube. kube-context=" + str(kube_context)\
                + ", repository-uri=" + str(repository_uri)\
                + ", kube-job-template-path=" + str(kube_job_template_path))

        from mlflow.projects.docker import (
            build_docker_image,
            validate_docker_env,
            validate_docker_installation,
        )
        from mlflow.projects import kubernetes as kb

        tracking.MlflowClient().set_tag(active_run.info.run_id, MLFLOW_PROJECT_ENV, "docker")
        validate_docker_env(project)
        validate_docker_installation()
        kube_config = mlflow.projects._parse_kubernetes_config(backend_config)
        image = build_docker_image(
            work_dir=work_dir,
            repository_uri=kube_config["repository-uri"],
            base_image=project.docker_env.get("image"),
            run_id=active_run.info.run_id,
        )
        image_digest = kb.push_image_to_registry(image.tags[0])
        submitted_run = self.run_kubernetes_job(
            project.name,
            active_run,
            image.tags[0],
            image_digest,
            get_entry_point_command(project, entry_point, params, backend_config['STORAGE_DIR']),
            get_run_env_vars(
                run_id=active_run.info.run_uuid, experiment_id=active_run.info.experiment_id
            ),
            kube_config.get("kube-context", None),
            kube_config["kube-job-template"],
        )
        return submitted_run

    def run_kubernetes_job(
        self,
        project_name,
        active_run,
        image_tag,
        image_digest,
        command,
        env_vars,
        kube_context=None,
        job_template=None,
    ):
        job_template = mlflow.projects.kubernetes._get_kubernetes_job_definition(
            project_name, image_tag, image_digest, _get_run_command(command), env_vars, job_template
        )
        job_name = job_template["metadata"]["name"]
        job_namespace = job_template["metadata"]["namespace"]
        _load_kube_context(context=kube_context)

        core_api_instance = kubernetes.client.CoreV1Api()
        tok = base64.b64encode(open(tokenfile.get_token_file_name(), "r").read().encode('utf-8')).decode('utf-8')
        try:
            core_api_instance.delete_namespaced_secret(namespace=job_namespace, name='infintokenfile')
        except:
            pass
        sec = kubernetes.client.V1Secret()
        sec.metadata = kubernetes.client.V1ObjectMeta(name='infintokenfile')
        sec.type = 'Opaque'
        sec.data = {'token': tok}
        core_api_instance.create_namespaced_secret(namespace=job_namespace, body=sec)
        aws_creds = base64.b64encode(open(os.path.join(expanduser('~'), '.aws', 'credentials'), "r").read().encode('utf-8')).decode('utf-8')
        try:
            core_api_instance.delete_namespaced_secret(namespace=job_namespace, name='awscredsfile')
        except:
            pass
        sec1 = kubernetes.client.V1Secret()
        sec1.metadata = kubernetes.client.V1ObjectMeta(name='awscredsfile')
        sec1.type = 'Opaque'
        sec1.data = {'credentials': aws_creds}
        core_api_instance.create_namespaced_secret(namespace=job_namespace, body=sec1)

        volume_mounts = [
                    kubernetes.client.V1VolumeMount(mount_path='/root/.infinstor', name='infin-token-file'),
                    kubernetes.client.V1VolumeMount(mount_path='/root/.aws', name='aws-creds-file')
                ]
        job_template["spec"]["template"]["spec"]["containers"][0]["volumeMounts"] = volume_mounts

        job_template["spec"]["template"]["spec"]["volumes"] = [
                    kubernetes.client.V1Volume(name="infin-token-file", secret=kubernetes.client.V1SecretVolumeSource(secret_name='infintokenfile')),
                    kubernetes.client.V1Volume(name="aws-creds-file", secret=kubernetes.client.V1SecretVolumeSource(secret_name='awscredsfile'))
                ]

        api_instance = kubernetes.client.BatchV1Api()
        api_instance.create_namespaced_job(namespace=job_namespace, body=job_template, pretty=True)

        return KubernetesSubmittedRun(active_run.info.run_id, job_name, job_namespace)
