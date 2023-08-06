# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rustlike']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rustlike',
    'version': '0.2.1',
    'description': 'Rust-like API in Python',
    'long_description': 'None',
    'author': 'Josh Wycuff',
    'author_email': 'Joshua.Wycuff@turner.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
