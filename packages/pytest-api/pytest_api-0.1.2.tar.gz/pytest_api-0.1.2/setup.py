# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_api']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'pytest>=7.1.1,<8.0.0']

setup_kwargs = {
    'name': 'pytest-api',
    'version': '0.1.2',
    'description': 'An ASGI middleware to populate OpenAPI Specification examples from pytest functions',
    'long_description': '# PyTest-API: Populate OpenAPI Examples from Python Tests\n\n![purpose](https://img.shields.io/badge/purpose-testing-green.svg)\n![PyPI](https://img.shields.io/pypi/v/pytest-api.svg)\n\nPyTest-API is an [ASGI middleware](https://asgi.readthedocs.io/en/latest/specs/main.html#middleware) that populates [OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification/) examples from [pytest](https://pypi.org/project/pytest/) functions. \n\n## Installation\n\n```shell\npip install pytest-api\n```\nor \n```\npoetry add --dev pytest-api\n```\n\n## How to use it:\n\nStarting with `test_main.py` file: \n\n```python\nfrom .main import spec\n\n\n@spec.describe\ndef test_default_route(client):\n    """\n    GIVEN\n    WHEN root endpoint is called with GET method\n    THEN response with status 200 and body OK is returned\n    """\n    response = client.get("/")\n    assert response.status_code == 200\n    assert response.json() == {"message": "OK"}\n```\n\nImpliment solution in `/main.py` file:\n\n```python\nfrom fastapi import FastAPI\n\nfrom pytest_api import SpecificationMiddleware\n\napp = FastAPI()\nspec = SpecificationMiddleware\n\napp.add_middleware(spec)\n\napp.openapi = spec.custom_openapi\n\n\n@app.get("/")\ndef default_route():\n    return {"message": "OK"}\n```\n\nRun FastAPI app:\n```bash\npoetry run uvicorn test_app.main:app --reload\n```\n\nOpen your browser to http://localhost:8000/docs#/ too find the doc string is populated into the description.\n\n![Your doc string will now be populated into the description.](./OpenAPI.png)',
    'author': 'Andrew Sturza',
    'author_email': 'sturzaam@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sturzaam/pytest-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
