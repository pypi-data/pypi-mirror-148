# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alfort']

package_data = \
{'': ['*']}

install_requires = \
['brython>=3.10.5,<4.0.0', 'conventional-commit>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'alfort',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'Masahiro Wada',
    'author_email': 'argon.argon.argon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
