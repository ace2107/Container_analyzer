import requests
import json
import re

internal_registry = "https://openshift.default.svc.cluster.local/oapi/v1/namespaces/dh-stage-jupyterhub/imagestreams"

api_url = "http://user-api-thoth-test-core.cloud.paas.upshift.redhat.com/api/v1/analyze"

headers = {'Authorization':'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJmcG9rb3JueS10aG90aC1kZXYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoiY29udGFpbmVyLWFuYWx5emVyLXNhLXRva2VuLTlrbGoyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImNvbnRhaW5lci1hbmFseXplci1zYSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjJlMWMzNTI4LWE1NjQtMTFlOC04NmExLWZhMTYzZThjMTg2MCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpmcG9rb3JueS10aG90aC1kZXY6Y29udGFpbmVyLWFuYWx5emVyLXNhIn0.fJpbAmHqBwPLBx08ea1kuINugQ4o52WJuTe2DY9-byLuZfSIPQ4CIWAhAtz6mN3EsyBrJyzrHIfcI_GCXm6gCjAHf0pDwUCMcVXfRRYX1OLlnGcg2CJUMUE5ma9v-woFZe8nFzm7IqQUuMWjygF09HzU8jsFPGqKwCdUh2i8B6w0JBust_oXz8T0xDYJYqnxQ87JELyLWL5o0_SU-TC26Fetl2nBCdgGvZh-9w2Gs5fPT03gBHwO46eWqnZfae-8aAWpxWFx6HIn2QmJPoxJYYOc1paa-k3qZwhXYqea7n3RXSGzjQ-Q-y8jBnTXkLQ0RrbWbG77FBv302wrY786nw'}

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
