import requests
import json
import re
import logging
import os
import sys

__version__ = '0.1'
__author__ = 'Akash Parekh <aparekh@redhat.com'
    
IMAGE_REGISTRY = "https://registry.upshift.redhat.com:8443/oapi/v1/projects"
API_URL = "http://user-api-thoth-test-core.cloud.paas.upshift.redhat.com/api/v1/analyze"
JH_REGISTRY = "https://openshift.default.svc.cluster.local/oapi/v1/namespaces/dh-stage-jupyterhub/imagestreams"

logging.basicConfig()
logger = logging.getLogger(__file__)

logger.setLevel(logging.DEBUG)

def analyze_registry_images():
    _SA_NAME = 'thoth-registry-view'
    _SA_TOKEN = os.getenv('REGISTRY_TOKEN')
    headers = {'Authorization':'Bearer %s' % _SA_TOKEN}
    response = requests.get(IMAGE_REGISTRY,headers = headers,verify = False)
    r = response.json()
    projectnames = []
    for doc in r["items"]:
        projectnames.append(doc["metadata"]["name"])
    
    imagenames = []
    namespaces = []
    for project in projectnames:
        REGISTRY_PROJECT = "https://registry.upshift.redhat.com:8443/oapi/v1/namespaces/%s/imagestreams"%project
        response = requests.get(REGISTRY_PROJECT,headers = headers,verify = False)
        r = response.json()
        for doc in r["items"]:
            imagenames.append(doc["metadata"]["name"])
            namespaces.append(doc["metadata"]["namespace"])

    for namespace_name,image_name in zip(namespaces,imagenames):
        DOCKER_IMAGE = 'docker-registry-default.cloud.registry.upshift.redhat.com/{}/{}'.format(namespace_name,image_name)
        PARAMS = (
        ('image', DOCKER_IMAGE),
        ('registry_user',_SA_NAME),
        ('registry_password',_SA_TOKEN),
        ('debug','true'),
        ('verify_tls','false')
        )
        r = requests.post(url=API_URL,params=PARAMS,verify = False)
        print(r.url)
        print(r.status_code)

def analyze_jh_images():
    _SA_TOKEN = os.getenv('JH_TOKEN')
    headers = {'Authorization':'Bearer %s' % _SA_TOKEN}
    response = requests.get(JH_REGISTRY,headers = headers,verify = False)
    r = response.json()
    containerimages = []
    for doc in r["items"]:
        containerimages.append(doc["status"]["dockerImageRepository"])
        print(containerimages)
    for image in containerimages:
        PARAMS = (
        ('image', image),
        ('registry_user','container-analyzer-sa'),
        ('registry_password',_SA_TOKEN),
        ('debug','true'),
        ('verify_tls','false')
        )
        resp = requests.post(url=api_url,params=PARAMS,verify = False)
        print(resp.url)
        print(resp.status_code)

def main():
    analyze_jh_images()
    analyze_registry_images()

if __name__ == '__main__':
    print("Running container-analyzer version", __version__)
    sys.exit(main())
