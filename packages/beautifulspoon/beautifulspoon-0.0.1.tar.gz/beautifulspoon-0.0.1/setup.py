# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['beautifulspoon']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10,<5.0']

entry_points = \
{'console_scripts': ['beautifulspoon = beautifulspoon.cli:main',
                     'bspoon = beautifulspoon.cli:main']}

setup_kwargs = {
    'name': 'beautifulspoon',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Gongziting Tech Ltd.',
    'author_email': None,
    'url': 'https://github.com/gzttech/beautifulspoon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
