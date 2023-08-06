# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_kexi']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.2,<8.0.0']

entry_points = \
{'pytest11': ['pytest-kexi = pytest_kexi.helper']}

setup_kwargs = {
    'name': 'pytest-kexi',
    'version': '0.10.0',
    'description': '',
    'long_description': None,
    'author': 'Kei Nakayama',
    'author_email': 'kei.of.nakayama@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
