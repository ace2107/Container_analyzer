import requests
import json
import re
from thoth.common import get_service_account_token

internal_registry = "https://openshift.default.svc.cluster.local/oapi/v1/namespaces/dh-stage-jupyterhub/imagestreams"

api_url = "http://user-api-fpokorny-thoth-dev.cloud.paas.upshift.redhat.com/api/v1/analyze"

API_TOKEN = get_service_account_token()
#add bearer token user end point
#namespace input taken from user
print(API_TOKEN)
print(type(API_TOKEN))
headers = {'Authorization':'Bearer %s' %API_TOKEN}

response1 = requests.get(internal_registry,headers = headers,verify = False)
response = response1.text

temp = re.findall(r'"dockerImageRepository":.(.*?)"tags',response)
images = []
for item in temp:
    a = item.replace('"','')
    b = a.replace("'","")
    c = b.replace(",","")
    d = c.replace(" ","")
    images.append(d)

for image in images:
    print(image)

for image in images:
    PARAMS = (
    ('image', image),
    ('debug', 'false'),
    ('verify-tls', 'false'),
    ('registry_user',''),
    ('registry_password',API_TOKEN)
    )

    r = requests.post(url=api_url,params=PARAMS,verify = False)
    print(r.url)
    print(r.status_code)
    analysis_results=r.json()
    print(analysis_results)
