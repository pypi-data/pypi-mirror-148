# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['globus_action_provider_tools_fastapi']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.2,<2.0.0',
 'boto3-stubs[essential]>=1,<2',
 'boto3>=1,<2',
 'fastapi>=0.75,<0.76',
 'globus-action-provider-tools>=0.12,<0.13']

setup_kwargs = {
    'name': 'globus-action-provider-tools-fastapi',
    'version': '0.1.0a1',
    'description': '',
    'long_description': None,
    'author': 'Jim Pruyne',
    'author_email': 'pruyne@uchicago.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
