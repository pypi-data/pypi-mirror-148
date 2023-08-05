# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aworda']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aworda',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Little-LinNian',
    'author_email': '2544704967@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
