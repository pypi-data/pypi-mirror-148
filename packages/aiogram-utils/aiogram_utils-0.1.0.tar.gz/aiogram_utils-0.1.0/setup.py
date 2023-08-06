# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_utils', 'aiogram_utils.filters', 'aiogram_utils.middlewares']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=2.20,<3.0', 'mongoengine>=0.24.1,<0.25.0']

setup_kwargs = {
    'name': 'aiogram-utils',
    'version': '0.1.0',
    'description': 'Misc utils for aiogram',
    'long_description': None,
    'author': 'levch',
    'author_email': 'levchenko.d.a1998@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
