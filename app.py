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
    watcher = kubernetes.watch.Watch()
    for event in watcher.stream(_K8S_API.list_namespaced_event,namespace=_NAMESPACE):
        for key,value in event:
            print(key,"\t",value,"\n")

if __name__ == '__main__':
    print("Running Container-analyzer version", __version__)
    sys.exit(main())
