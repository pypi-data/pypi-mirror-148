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
    'version': '0.1.7',
    'description': 'FlatQube API client library and CLI tools',
    'long_description': '# flatqube-client\n\n[![PyPI version](https://img.shields.io/pypi/v/flatqube-client.svg)](https://pypi.python.org/pypi/flatqube-client)\n![Supported Python versions](https://img.shields.io/pypi/pyversions/flatqube-client.svg)\n[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\nflatqube-client is an API client library and CLI tools for [FlatQube](https://app.flatqube.io) DEX service in [Everscale](https://everscale.network) blockchain network.\n\n## Installing\n\n```\npip3 install -U flatqube-client\n```\n\n## Usage\n\nMain CLI help:\n\n```\nflatqube --help\n```\n\n### Show Currency Info\n\nShow selected currencies:\n\n```\nflatqube currency show wever qube bridge\n```\n\nShow the default list (`everscale`) of currencies:\n\n```\nflatqube currency show\n```\n\nAlso, we can show some list, "star" for example:\n\n```\nflatqube currency show -l star\n```\n\n![2022-04-27_20-34-34](https://user-images.githubusercontent.com/1299189/165585978-08d49363-7f0f-408b-ba33-e55cae3c630d.png)\n\nOr we can show meme tokens sorted by price change:\n\n```\nflatqube currency show -l meme -s price-ch\n```\n\n![2022-04-27_20-58-13](https://user-images.githubusercontent.com/1299189/165589946-e9d1c943-ee13-4689-bf94-c45476674b8c.png)\n\nAlso, we can run cli in "auto-update" mode. By default update interval is 5 seconds:\n\n```\nflatqube currency show -l all -s price-ch -u -i3\n```\n\nSee help for more info about `currency show` command:\n\n```\nflatqube currency show --help\n```\n\n## License\n\n[MIT](https://opensource.org/licenses/MIT)\n',
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
