# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dubletten_tool', 'dubletten_tool.migrations']

package_data = \
{'': ['*'], 'dubletten_tool': ['static/dubletten_tool/css/*', 'templates/*']}

setup_kwargs = {
    'name': 'dubletten-tool',
    'version': '0.1.1',
    'description': 'APIS module for the VieCPro instance to perform manual deduplication of person instances',
    'long_description': None,
    'author': 'Gregor Pirgie',
    'author_email': 'gregor.pirgie@oeaw.ac.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
