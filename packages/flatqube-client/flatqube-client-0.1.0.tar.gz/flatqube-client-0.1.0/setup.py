# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flatqube']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=8.1.2,<9.0.0',
 'humanize>=4.0.0,<5.0.0',
 'omegaconf>=2.2.0,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['flatqube = flatqube.cli:cli']}

setup_kwargs = {
    'name': 'flatqube-client',
    'version': '0.1.0',
    'description': 'FlatQube API client library and CLI tools',
    'long_description': '# flatqube-client\n\nflatqube-client is an API client library and CLI tools for [FlatQube](https://app.flatqube.io) DEX service in [Everscale](https://everscale.network) blockchain network.\n',
    'author': 'Evgeny Prilepin',
    'author_email': 'esp.home@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
