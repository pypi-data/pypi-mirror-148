# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['let_me_google_that_for_you',
 'let_me_google_that_for_you.let_me_google_that_for_you']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'let-me-google-that-for-you',
    'version': '0.0.2',
    'description': 'Package',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
