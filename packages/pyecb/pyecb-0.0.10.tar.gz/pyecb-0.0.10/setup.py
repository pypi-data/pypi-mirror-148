# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyecb']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.3.0,<2.0.0',
 'poetry-dynamic-versioning>=0.14.1,<0.15.0',
 'pytest-cov>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'pyecb',
    'version': '0.0.10',
    'description': '',
    'long_description': None,
    'author': 'Matthew Macdonald-Wallace',
    'author_email': 'matt@doics.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
