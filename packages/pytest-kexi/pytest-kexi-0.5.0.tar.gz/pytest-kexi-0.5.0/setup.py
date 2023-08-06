# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_kexi']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.7.0,<2.0.0', 'setuptools>=62.1.0,<63.0.0']

setup_kwargs = {
    'name': 'pytest-kexi',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'Kei Nakayama',
    'author_email': 'kei.of.nakayama@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
