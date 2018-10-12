import requests
import json
import re
import logging

IMAGE_REGISTRY = "https://registry.upshift.redhat.com:8443/oapi/v1/projects"
API_URL = "http://user-api-thoth-test-core.cloud.paas.upshift.redhat.com/api/v1/analyze"
SA_NAME = 'thoth-registry-view'
logging.basicConfig()
logger = logging.getLogger(__file__)

logger.setLevel(logging.DEBUG)
try:
    logger.debug('Trying to get bearer token from secrets file within pod...')
    with open('/var/run/secrets/kubernetes.io/dockerconfigjson/upshift') as f:
        SA_TOKEN_TEST = f.read()
        print(SA_TOKEN_TEST)
except:
    logger.info("Not running within correct OpenShift cluster...")

try:
    logger.debug('Trying to get bearer token from secrets file within pod...')
    with open('/var/run/secrets/openshift.io/build/upshift') as f:
        SA_TOKEN_TEST = f.read()
        print(SA_TOKEN_TEST)
except:
    logger.info("Not running within correct OpenShift cluster...")

SA_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJ0aG90aC1zdGF0aW9uIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6InRob3RoLXJlZ2lzdHJ5LXZpZXctdG9rZW4tZms3azUiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidGhvdGgtcmVnaXN0cnktdmlldyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijc0NTVjNDNmLWM3MDAtMTFlOC04MTRjLWZhMTYzZTA5Y2U2NSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDp0aG90aC1zdGF0aW9uOnRob3RoLXJlZ2lzdHJ5LXZpZXcifQ.b2OQAu-cXLVyAEjPdAOLIaHCoxGNrjZeWddiBS7uFzEnVi8hZLcRRASMVt4IOcnZRM5hDaqHcuDGu9ywWpHzVcvPKVddOv3CTboYxtd7N4PjnLmmxv1YEqSe0Si05ebd4oX1d6udX6iGa0KW8WZlKdvzL_4tfVJisdS5TTqvKcjayDpJ4PtbwfV59Pl5PLATAn5Rg56BR5RnK3Q-UMqVqdI-Ujyhjnyd5t1RtSaoywKtFr8v0Jawb5SYGc0D8_r7HL3l1M52M_UI2OxaAgIuIJN4RM8unWri8UZ9CKwFvRY718pnDUikl_svaEbu7S2PPK4zKXQdPWvD7_95m4IF0g'
headers = {'Authorization':'Bearer %s' % SA_TOKEN}

if(SA_TOKEN_TEST==SA_TOKEN):
    print("GIMMEEE A HELL YEAHH !")
else:
    print("oops")

response = requests.get(IMAGE_REGISTRY,headers = headers,verify = False)
r = response.json()

projectnames = []
for doc in r["items"]:
    projectnames.append(doc["metadata"]["name"])

imagenames = []
namespaces = []
for project in projectnames:
    registrylink = "https://registry.upshift.redhat.com:8443/oapi/v1/namespaces/%s/imagestreams"%project
    response = requests.get(registrylink,headers = headers,verify = False)
    r = response.json()
    for doc in r["items"]:
        imagenames.append(doc["metadata"]["name"])
        namespaces.append(doc["metadata"]["namespace"])

for namespace_name,image_name in zip(namespaces,imagenames):
    DOCKER_IMAGE = 'docker-registry-default.cloud.registry.upshift.redhat.com/{}/{}'.format(namespace_name,image_name)
    PARAMS = (
    ('image', DOCKER_IMAGE),
    ('registry_user',SA_NAME),
    ('registry_password',SA_TOKEN),
    ('debug','false'),
    ('verify_tls','false')
    )
    r = requests.post(url=API_URL,params=PARAMS,verify = False)
    print(r.url)
    print(r.status_code)
