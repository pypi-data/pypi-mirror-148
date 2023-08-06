# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_kexi']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.7.0,<2.0.0']

entry_points = \
{'pytest11': ['pytest_kexi = pytest_kexi.helper']}

setup_kwargs = {
    'name': 'pytest-kexi',
    'version': '0.7.37',
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
