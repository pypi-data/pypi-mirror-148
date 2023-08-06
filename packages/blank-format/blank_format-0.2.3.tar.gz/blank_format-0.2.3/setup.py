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
    'version': '0.2.3',
    'description': 'The ultimate code formatter',
    'long_description': '# Blank\n\nThe ultimate Python code formatter!\n\nIt will recurse and clean all your .py files.\n\nBenefits:\n\n- Identical formatting in every file!\n- No code => no bugs!\n\n[![asciicast](blank.svg)](https://asciinema.org/a/jHwPoOilk3Pinvh3fYOXQgdr1)\n\n## Installation\n\n    pip install blank-format\n    \n## Usage\n\n    blank\n',
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
