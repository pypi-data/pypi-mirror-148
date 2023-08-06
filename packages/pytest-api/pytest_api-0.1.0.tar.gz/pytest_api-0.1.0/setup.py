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
    'version': '0.1.0',
    'description': 'An ASGI middleware to populate OpenAPI Specification examples from pytest functions',
    'long_description': None,
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
