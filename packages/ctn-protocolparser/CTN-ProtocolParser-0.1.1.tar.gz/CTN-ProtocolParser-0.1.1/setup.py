# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protocol_parser']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.2,<2.0.0']

entry_points = \
{'console_scripts': ['protocol_parser = protocol_parser.cli:main']}

setup_kwargs = {
    'name': 'ctn-protocolparser',
    'version': '0.1.1',
    'description': 'Utility to parse protocols for the CTN islets framework.',
    'long_description': None,
    'author': 'Johannes Pfabe',
    'author_email': '39130094+Hannnsen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Hannnsen/protocol_parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
