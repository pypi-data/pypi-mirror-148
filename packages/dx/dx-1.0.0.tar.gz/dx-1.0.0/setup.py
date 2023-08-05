# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dx']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'dx',
    'version': '1.0.0',
    'description': 'Python wrapper for Data Explorer',
    'long_description': None,
    'author': 'Dave Shoup',
    'author_email': 'dave.shoup@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.7,<4.0.0',
}


setup(**setup_kwargs)
