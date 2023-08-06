# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['empirelang']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'empirelang',
    'version': '0.1.0.1',
    'description': 'The Empire language',
    'long_description': None,
    'author': 'What_do_we_do_now',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
