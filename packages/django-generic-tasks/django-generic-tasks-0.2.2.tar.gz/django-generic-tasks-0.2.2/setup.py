# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_generic_tasks', 'django_generic_tasks.migrations']

package_data = \
{'': ['*']}

install_requires = \
['CacheControl>=0.12.11,<0.13.0',
 'Django>=4.0.4,<5.0.0',
 'django-ninja>=0.17.0,<0.18.0',
 'google-auth>=2.6.6,<3.0.0',
 'google-cloud-tasks>=2.8.1,<3.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'django-generic-tasks',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'Jiayu Yi',
    'author_email': 'yijiayu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
