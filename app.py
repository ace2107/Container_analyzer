import requests
import json
import re

internal_registry = "https://openshift.default.svc.cluster.local/oapi/v1/namespaces/dh-stage-jupyterhub/imagestreams"

api_url = "http://user-api-thoth-test-core.cloud.paas.upshift.redhat.com/api/v1/analyze"

headers = {'Authorization':'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJ0aG90aC10ZXN0LWNvcmUiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoiY29udGFpbmVyLWFuYWx5emVyLXRva2VuLTIyeDd2Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImNvbnRhaW5lci1hbmFseXplciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImFjNzU0ZDQ5LTg0NWItMTFlOC1iNWZiLWZhMTYzZThjMTg2MCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDp0aG90aC10ZXN0LWNvcmU6Y29udGFpbmVyLWFuYWx5emVyIn0.OXXbIfvCA1sSlDyc3YvMfvPwpNk8y1b4N22aPeGGQJMPpnwIReVD-Ut9Y75xvz4Oh8ywBJETXnqYJH66C4PGILF8bKv7F9-3ishqtsXlUXMrd7gxqvvn8wFQMp3pgLcsDpLx3EQi_duklF1o54V3i90MRHXLPrEiMJizxFA4auKRGm-TmbPIa_8bBrfRZiVpmyBq4oj2WasGJm56HmjB9lyCzbM4VUflWLELXxgAwwXmeSP3oPAyMDvFYhetap1AiX4LNqhUA-p_Iu0Ay701snTuOktAypQxJk5qlHgaCbQK5rjj9rA2vdyin7ww9437bTQbtFPQf3YcDba5U4jtIw'}

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
analyzer = 'fridex/thoth-package-extract'

HEADERS = {
    'Content-Type':'application/json',
    'Accept':'application/json',
}

for image in images:
    PARAMS = (
    ('image', image),
    ('analyzer', analyzer),
    ('debug', 'false'),
    ('verify-tls', 'false'),
    )

    r = requests.post(url=api_url,params=PARAMS,headers=HEADERS,timeout=10,verify = False)
    print(r.url)
    print(r.status_code)
    analysis_results=r.json()
    print(analysis_results)
