# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clockify',
 'clockify.apis',
 'clockify.model',
 'clockify.user',
 'clockify.user.membership',
 'clockify.user.settings',
 'clockify.user.settings.summaryreportsettings']

package_data = \
{'': ['*']}

install_requires = \
['bidict>=0.22.0,<0.23.0',
 'marshmallow>=3.15.0,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'clockify-api',
    'version': '0.1.0',
    'description': "Python wrapper for Clockify's API.",
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
