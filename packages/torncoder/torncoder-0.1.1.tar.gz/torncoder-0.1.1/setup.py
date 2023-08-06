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
    'version': '0.1.1',
    'description': 'Basic tornado-based python utilities.',
    'long_description': "# Torncoder\n\nTornado Utility Library for various features.\n\nThis library contains a few common classes and helpers that:\n - Make file serving easier.\n - Make file uploads easier.\n - Permit piping output from processes easier.\n - Basic pool management.\n\n## (Static) FileHandler Utilities\n\n`tornado`'s default `web.StaticFileHandler` is a bit onerous and confusing to\nsubclass or otherwise use; `torncoder` instead defines a slightly different\ninterface for similar purposes, but consolidates much of the work:\n\n```python\nclass MyFileHandler(AbstractFileHandler):\n\n    async def fetch_file_info(self, path):\n        # Validate path, then return a FileInfo tuple.\n        return FileInfo(...)\n\n    async def get_iter_content(self, path_handle, start, end):\n        # Iterate over the content from start/end.\n        # NOTE: 'path_handle' is the path argument by the above FileInfo.\n```\n",
    'author': 'Aaron Gibson',
    'author_email': 'eulersidcrisis@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eulersIDcrisis/torncoder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
