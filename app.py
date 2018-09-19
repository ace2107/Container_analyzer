#!/usr/bin/env python3
#To be continued
#see app-job.py to run cronjob
__version__ = '0.0.1'
__author__ = 'Akash Parekh <aparekh@redhat.com>'

import os
import sys
import logging
from pathlib import Path

import requests
import json

import daiquiri
import kubernetes
import openshift

daiquiri.setup(level=logging.DEBUG if bool(int(os.getenv('DEBUG-CONTAINER-ANALYZER', 0))) else logging.INFO)

# Load in-cluster configuration that is exposed by OpenShift/k8s configuration.
kubernetes.config.load_incluster_config()

_LOGGER = logging.getLogger('container-analyzer')
_NAMESPACE = "dh-stage-jupyterhub"
#_NAMESPACE = Path('/run/secrets/kubernetes.io/serviceaccount/namespace').read_text()
_K8S_API = kubernetes.client.CoreV1Api()
_OCP_BUILD = openshift.client.BuildOpenshiftIoV1Api(openshift.client.ApiClient())

"""
# Payload sent to trigger analysis.
_PAYLOAD = {
    "kind": "BuildRequest",
    "apiVersion": "build.openshift.io/v1",
    "metadata": {
        "name": "XXX",
    },
    "triggeredBy": [{
        "message": "DownShift triggered"
    }],
    "dockerStrategyOptions": {},
    "sourceStrategyOptions": {}
}
"""
def main():
    oapi = openshift.client.OapiApi()
    #watcher = kubernetes.watch.Watch()
    project_list = oapi.list_project()
    configuration = openshift.client.Configuration()

    api_instance = openshift.client.ImageOpenshiftIoV1Api(openshift.client.ApiClient(configuration))
    namespace = 'dh-stage-jupyterhub' # str | object name and auth scope, such as for teams and projects

    try:
        api_response = api_instance.list_namespaced_image_stream(namespace, pretty=pretty, _continue=_continue, field_selector=field_selector, include_uninitialized=include_uninitialized, label_selector=label_selector, limit=limit, resource_version=resource_version, timeout_seconds=timeout_seconds, watch=watch)
        print(api_response)
    except ApiException as e:
        print("Exception when calling ImageOpenshiftIoV1Api->list_namespaced_image_stream: %s\n" % e)

    for project in project_list.items:
        print(project.metadata.name)
    
    api_instance3 = openshift.client.AdmissionregistrationApi()
    try:
        api_response3 = api_instance3.get_api_group()
        print(api_response3)
    except APIException as e:
        print("Exception when calling AdmissionregistrationApi->get_api_group: %s\n" % e)
    #for event in watcher.stream(_K8S_API.list_namespaced_event,namespace=_NAMESPACE):
        #print(event)
        #print(type(event))

if __name__ == '__main__':
    print("Running Container-analyzer version", __version__)
    sys.exit(main())
