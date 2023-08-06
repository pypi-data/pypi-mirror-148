# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vlcsync']

package_data = \
{'': ['*']}

install_requires = \
['cached-property', 'loguru', 'psutil']

entry_points = \
{'console_scripts': ['vlcsync = vlcsync.main:main']}

setup_kwargs = {
    'name': 'vlcsync',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'mrkeuz',
    'author_email': 'mrkeuz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
