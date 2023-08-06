# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rdr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rdr',
    'version': '0.1.0',
    'description': 'Research design records',
    'long_description': None,
    'author': 'Andrew Stewart',
    'author_email': 'andrew.c.stewart@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
