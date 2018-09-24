import requests
import json
import re
from thoth.common import get_service_account_token

#add name of namespace as variable
internal_registry = "https://registry-console-default.cloud.registry.upshift.redhat.com/registry#/images/thoth-station"
api_url = "http://user-api-fpokorny-thoth-dev.cloud.paas.upshift.redhat.com/api/v1/analyze"

API_TOKEN = get_service_account_token()
headers = {'Authorization':'Bearer %s' %API_TOKEN}

response = requests.get(internal_registry,header = headers,verify = False)
print(response)
print(response.status_code)
print(response.url)
r = response.json()

print(json.dumps(r, indent = 4,sort_keys = True))
print(response.url)
print(response.status_code)

containerimages = []
imageshashes = []
#use only latest image hash
for doc in r["items"]:
        containerimages.append(doc["status"]["dockerImageRepository"])
        print(doc["status"]["dockerImageRepository"])
        for l in doc["status"]["tags"]:
                for k in l["items"]:
                        imageshashes.append(k["image"])
                        print(k["image"])
        print("\n \n ")

#name of sa
for image in containerimages:
    PARAMS = (
    ('image', image),
    ('registry_user','container-analyzer-sa'),
    ('registry_password',API_TOKEN),
    ('debug','true'),
    ('verify_tls','false')
    )

    resp = requests.post(url=api_url,params=PARAMS,verify = False)
    print(resp.url)
    print(resp.status_code)
    analysis_results=r.json()
    print(analysis_results)
