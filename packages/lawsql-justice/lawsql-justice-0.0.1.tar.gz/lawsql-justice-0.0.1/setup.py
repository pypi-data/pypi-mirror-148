# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lawsql_justice']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lawsql-justice',
    'version': '0.0.1',
    'description': 'Pattern matching for Justices',
    'long_description': '# LawSQL Justice Patterns\n\nSome common patterns.\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
