import requests
import json
import re
from thoth.common import get_service_account_token
import logging

image_registry = "https://registry.upshift.redhat.com:8443/oapi/v1/projects"
api_url = "http://user-api-thoth-test-core.cloud.paas.upshift.redhat.com/api/v1/analyze"

logging.basicConfig()
logger = logging.getLogger(__file__)

logger.setLevel(logging.DEBUG)

try:
    logger.debug('Trying to get bearer token from secrets file within pod...')
    with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as f:
        SA_TOKEN = f.read()
except:
    logger.info("Not running within correct OpenShift cluster...")

SA_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJ0aG90aC1zdGF0aW9uIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6InRob3RoLXJlZ2lzdHJ5LXZpZXctdG9rZW4tY3BzNngiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidGhvdGgtcmVnaXN0cnktdmlldyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijc0NTVjNDNmLWM3MDAtMTFlOC04MTRjLWZhMTYzZTA5Y2U2NSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDp0aG90aC1zdGF0aW9uOnRob3RoLXJlZ2lzdHJ5LXZpZXcifQ.gIDoY8rOMpryer4cANjWC54x4VJOoLHO0bzRLp1OSa9wi4s0KDfeHLje-KtoekGIdAWt2qdUQbC1yFCYLSsK3Q5ofA-HdYZkQo7wkpIjrnE-WlC2C_JovhIhO8j1g-EVzTgVlKKrnrQoq_r970HyE-pIPctFvL0ZsH4JQGEGQrQBLrLKp19q9DKu85DVjmbo0dNZOe13dID6VcnUbpMOobaBsteOzfIu5jEPRvbZEocTEzCnsQFd1qlax5SLRAMXByQH8cHeMbraK4m68712gOR2moyTlzRF7kdPO-aWzQJLN3IP1ZwLVdcRRt0SK9QMepgmeb6laz1bGkRYw8iAng'
headers = {'Authorization':'Bearer %s' % SA_TOKEN}

response = requests.get(image_registry,headers = headers,verify = False)
r = response.json()

projectnames = []
containerimages = []
imageshashes = []

for doc in r["items"]:
    projectnames.append(doc["metadata"]["name"])

for project in projectnames:
    registrylink = "https://registry.upshift.redhat.com:8443/oapi/v1/namespaces/%s/imagestreams"%project
    response = requests.get(registrylink,headers = headers,verify = False)
    r = response.json()
    for doc in r["items"]:
        containerimages.append(doc["status"]["dockerImageRepository"])
        for key in doc["status"]:
            """
            #ask frido
                for l in doc["status"]["tags"]:
                    for k in l["items"]:
                        imageshashes.append(k["image"])
                        print(k["image"])
            """

for image in containerimages:
    PARAMS = (
    ('image', image),
    ('registry_user','thoth-registry-view'),
    ('registry_password',SA_TOKEN),
    ('debug','true'),
    ('verify_tls','false')
    )

    r = requests.post(url=api_url,params=PARAMS,verify = False)
    print(r.url)
    print(r.status_code)