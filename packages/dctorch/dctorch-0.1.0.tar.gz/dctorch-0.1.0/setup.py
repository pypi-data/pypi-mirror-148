# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dctorch']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'scipy>=1.8.0,<2.0.0', 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'dctorch',
    'version': '0.1.0',
    'description': 'fast discrete cosine transforms for pytorch',
    'long_description': None,
    'author': 'jack',
    'author_email': 'jack@gallabytes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
