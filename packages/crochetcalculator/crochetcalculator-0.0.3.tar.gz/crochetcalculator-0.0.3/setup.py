# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crochetcalculator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'crochetcalculator',
    'version': '0.0.3',
    'description': 'Calculate crochet patterns',
    'long_description': '# Crochet Calculator\nThe crochet calculator is a handy tool that can be used to calculate crochet gauge and generate simple crochet patterns.\n\n## Installation\nYou can install the Crochet Calculator from PyPI:\n\n    pip install crochetcalculator\n\n<!-- \n## Example usage\n\n## Contributing\n\n### Setting up the development environment\n\n## Change log\n\n## License and author info \n-->',
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
