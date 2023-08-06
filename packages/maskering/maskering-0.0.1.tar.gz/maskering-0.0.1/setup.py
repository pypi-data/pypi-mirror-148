# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maskering']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'maskering',
    'version': '0.0.1',
    'description': 'maskering av tekster',
    'long_description': None,
    'author': 'pbencze',
    'author_email': 'paul@idelab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
