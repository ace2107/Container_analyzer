import requests

internal_registry = "docker-registry.default.svc:5000/dh-stage-jupyterhub/*"

api_url = "http://user-api-thoth-test-core.cloud.paas.upshift.redhat.com/api/v1/ui/#/"


images = ['fedora:28','fedora:27','fedora:26']
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
	analysis_results=r.json()
	print(analysis_results)
