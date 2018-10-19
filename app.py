#!/usr/bin/env python3
"""Fetches container images from registry and sends them for analysis"""
import os
import sys
import logging

import requests

__version__ = '0.1'
__author__ = 'Akash Parekh <aparekh@redhat.com'

IMAGE_REGISTRY = "https://registry.upshift.redhat.com:8443/oapi/v1/projects"
API_URL = "http://user-api-thoth-test-core.cloud.paas.upshift.redhat.com/api/v1/analyze"
JH_REGISTRY = "https://openshift.default.svc.cluster.local/oapi/v1/namespaces/dh-stage-jupyterhub/imagestreams"

logging.basicConfig()
_LOGGER = logging.getLogger(__file__)

_LOGGER.setLevel(logging.DEBUG)

def analyze_registry_images():
    """Function to get registry images and send for analysis"""
    _SA_NAME = 'thoth-registry-view'
    _SA_TOKEN = os.getenv('REGISTRY_TOKEN')
    if not _SA_TOKEN:
        print("Please provide service account bearer tokens for upshift registry")
        return
    headers = {'Authorization':'Bearer %s' % _SA_TOKEN}
    response = requests.get(IMAGE_REGISTRY, headers=headers, verify=False)
    resp = response.json()
    projectnames = []
    for doc in resp["items"]:
        projectnames.append(doc["metadata"]["name"])
    imagenames = []
    namespaces = []
    for project in projectnames:
        registry_project = "https://registry.upshift.redhat.com:8443/oapi/v1/namespaces/%s/imagestreams"%project
        response = requests.get(registry_project, headers=headers, verify=False)
        resp = response.json()
        for doc in resp["items"]:
            imagenames.append(doc["metadata"]["name"])
            namespaces.append(doc["metadata"]["namespace"])
    for namespace_name, image_name in zip(namespaces, imagenames):
        registry_image_name = 'docker-registry-default.cloud.registry.upshift.redhat.com/{}/{}'.format(namespace_name, image_name)
        parameters = (
            ('image', registry_image_name),
            ('registry_user', _SA_NAME),
            ('registry_password', _SA_TOKEN),
            ('debug', 'true'),
            ('verify_tls', 'false')
            )
        resp = requests.post(url=API_URL, params=parameters, verify=False)
        print(resp.status_code)

def analyze_jh_images():
    """Function to get images from dh-stage-jupyterhub and send for analysis"""
    _SA_TOKEN = os.getenv('JH_TOKEN')
    if not _SA_TOKEN:
        print("Please provide service account bearer tokens for dh-stage-jupyterhub")
        return
    headers = {'Authorization':'Bearer %s' % _SA_TOKEN}
    response = requests.get(JH_REGISTRY, headers=headers, verify=False)
    resp = response.json()
    containerimages = []
    for doc in resp["items"]:
        containerimages.append(doc["status"]["dockerImageRepository"])
    for image in containerimages:
        parameters = (
            ('image', image),
            ('registry_user', 'container-analyzer-sa'),
            ('registry_password', _SA_TOKEN),
            ('debug', 'true'),
            ('verify_tls', 'false')
            )
        resp = requests.post(url=API_URL, params=parameters, verify=False)
        print(resp.status_code)

def main():
    """Main function"""
    analyze_jh_images()
    analyze_registry_images()

if __name__ == '__main__':
    print("Running container-analyzer version", __version__)
    sys.exit(main())
