# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argus',
 'argus.backend',
 'argus.backend.controller',
 'argus.backend.service',
 'argus.db']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.4.1', 'pydantic==1.8.2', 'scylla-driver==3.24.8']

setup_kwargs = {
    'name': 'argus-alm',
    'version': '0.7.1',
    'description': 'Argus',
    'long_description': 'None',
    'author': 'Alexey Kartashov',
    'author_email': 'alexey.kartashov@scylladb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
