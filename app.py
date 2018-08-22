import requests
import json
import re

internal_registry = "https://openshift.default.svc.cluster.local/oapi/v1/namespaces/dh-stage-jupyterhub/imagestreams"

api_url = "http://user-api-fpokorny-thoth-dev.cloud.paas.upshift.redhat.com/api/v1/analyze"

API_TOKEN = get_service_account_token()

def get_service_account_token():
    """Get token from service account token file."""
    try:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token_file:
            return token_file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Unable to get service account token, please check "
                                "that service has service account assigned with exposed token") from exc
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
    ('registry_user','container-analyzer-sa'),
    ('registry_password',API_TOKEN)
    )

    r = requests.post(url=api_url,params=PARAMS,verify = False)
    print(r.url)
    print(r.status_code)
    analysis_results=r.json()
    print(analysis_results)
