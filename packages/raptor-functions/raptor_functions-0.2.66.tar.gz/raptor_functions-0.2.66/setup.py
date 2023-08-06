# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raptor_functions',
 'raptor_functions.examples',
 'raptor_functions.supervised',
 'raptor_functions.unsupervised']

package_data = \
{'': ['*'],
 'raptor_functions': ['dev/*',
                      'eda/*',
                      'ensemble/*',
                      'nn/*',
                      'rapmon/*',
                      'semi_supervised/*'],
 'raptor_functions.examples': ['plots/*']}

setup_kwargs = {
    'name': 'raptor-functions',
    'version': '0.2.66',
    'description': 'raptor functions',
    'long_description': None,
    'author': 'Daniel Fiuza, Ibrahim Animashaun',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Bryant-Dental/raptor_functions.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
