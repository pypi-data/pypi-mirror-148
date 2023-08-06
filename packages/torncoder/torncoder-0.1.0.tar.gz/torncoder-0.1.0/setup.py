# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torncoder', 'torncoder.file_util']

package_data = \
{'': ['*']}

install_requires = \
['aiofile>=3.7.4,<4.0.0', 'tornado>=6.1,<7.0']

setup_kwargs = {
    'name': 'torncoder',
    'version': '0.1.0',
    'description': 'Basic tornado-based python utilities.',
    'long_description': None,
    'author': 'Aaron Gibson',
    'author_email': 'eulersidcrisis@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
