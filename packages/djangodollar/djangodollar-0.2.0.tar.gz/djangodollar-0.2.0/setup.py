# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangodollar']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.4,<5.0.0']

setup_kwargs = {
    'name': 'djangodollar',
    'version': '0.2.0',
    'description': 'A simple package for working with dollar amounts in Django.',
    'long_description': None,
    'author': 'Ethan Corey',
    'author_email': 'ethanscorey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
