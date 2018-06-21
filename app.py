import requests
import json

#registry = "https://openshift.default.svc.cluster.local"
api_url = "http://user-api-thoth-test-core.cloud.upshift.engineering.redhat.com/api/v1/analyze"


images = ['fedora:28','fedora27','fedora26']
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
    ('verify-tls', 'true'),
    )

	r = requests.post(url=api_url,params=PARAMS,headers=HEADERS,timeout=10)
	print(r.status_code)
	r.raise_for_status()
	analysis_results=r.json()
	print(analysis_results)