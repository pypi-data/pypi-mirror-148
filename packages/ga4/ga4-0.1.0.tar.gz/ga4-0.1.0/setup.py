# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ga4', 'ga4.log']

package_data = \
{'': ['*']}

install_requires = \
['google-analytics-data>=0.11.2,<0.12.0',
 'pandas>=1.4.2,<2.0.0',
 'pyspark>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'ga4',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 's4mukka',
    'author_email': 'meninosam197@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
