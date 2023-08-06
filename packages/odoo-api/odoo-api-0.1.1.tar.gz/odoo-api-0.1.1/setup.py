# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odoo']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'simplejson>=3.17.6,<4.0.0']

setup_kwargs = {
    'name': 'odoo-api',
    'version': '0.1.1',
    'description': 'Api wrapper for Odoo 14.',
    'long_description': None,
    'author': 'Jean-Paul Weijers',
    'author_email': 'jpweijers@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
