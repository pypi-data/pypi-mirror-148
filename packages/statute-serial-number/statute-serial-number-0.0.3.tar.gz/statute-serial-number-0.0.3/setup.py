# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statute_serial_number']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'statute-serial-number',
    'version': '0.0.3',
    'description': 'Uniform serialization of Statutes that map to STATUTEPATH directory',
    'long_description': 'None',
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
