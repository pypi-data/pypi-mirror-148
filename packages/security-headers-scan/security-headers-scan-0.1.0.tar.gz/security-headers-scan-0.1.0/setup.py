# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['security_headers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'certifi>=2021.10.8,<2022.0.0',
 'click>=8.0.3,<9.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.27.1,<3.0.0',
 'semantic-version>=2.9.0,<3.0.0']

setup_kwargs = {
    'name': 'security-headers-scan',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pat',
    'author_email': 'patrick.turner@nhs.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
