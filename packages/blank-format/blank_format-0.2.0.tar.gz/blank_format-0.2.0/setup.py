# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blank_format']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['blank = blank_format:main']}

setup_kwargs = {
    'name': 'blank-format',
    'version': '0.2.0',
    'description': 'The ultimate code formatter',
    'long_description': None,
    'author': 'Joni Turunen',
    'author_email': 'rojun.itu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d3rp/blank',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
