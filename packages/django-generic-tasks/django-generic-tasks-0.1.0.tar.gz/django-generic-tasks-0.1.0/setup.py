# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_generic_tasks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-generic-tasks',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jiayu Yi',
    'author_email': 'yijiayu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
