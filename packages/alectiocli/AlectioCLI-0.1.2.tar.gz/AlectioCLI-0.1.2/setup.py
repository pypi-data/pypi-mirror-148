# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alectiocli',
 'alectiocli.src',
 'alectiocli.src.experiment',
 'alectiocli.src.hybrid_labeling',
 'alectiocli.src.project']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'alectio-sdk>=0.6.21,<0.7.0',
 'inquirer>=2.9.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.2.0,<13.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['alectio-cli = alectiocli.main:app']}

setup_kwargs = {
    'name': 'alectiocli',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'Adwitiya',
    'author_email': 'adwitiya.trivedi@alectio.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
