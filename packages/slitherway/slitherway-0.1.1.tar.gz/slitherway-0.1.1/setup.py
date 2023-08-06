# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slitherway']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'slitherway',
    'version': '0.1.1',
    'description': 'Python wrapper for the Flyway CLI',
    'long_description': None,
    'author': 'Ryan Brink',
    'author_email': 'rbweb@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
