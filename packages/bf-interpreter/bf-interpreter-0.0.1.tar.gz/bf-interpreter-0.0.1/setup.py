# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bf_interpreter']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bf = bf_interpreter.main:main']}

setup_kwargs = {
    'name': 'bf-interpreter',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Bruno Silva Oliveira',
    'author_email': 'brunooliveira095@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
