# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crochetcalculator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'crochetcalculator',
    'version': '0.0.2',
    'description': 'Calculate crochet patterns',
    'long_description': None,
    'author': 'alicew',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
