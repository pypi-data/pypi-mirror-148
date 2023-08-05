# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tuify']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.0.0,<13.0.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.10.0,<4.0.0']}

setup_kwargs = {
    'name': 'tuify',
    'version': '0.1.0',
    'description': 'Transforming Python CLIs into TUIs',
    'long_description': None,
    'author': 'alwinw',
    'author_email': '16846521+alwinw@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
