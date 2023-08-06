# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tuify']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.0.0,<13.0.0']

setup_kwargs = {
    'name': 'tuify',
    'version': '0.1.0.post3',
    'description': 'Transforming Python CLIs into TUIs',
    'long_description': '# tuify\n\nTransforming Python CLIs into TUIs\n\n:warning: _This package is currently under development_\n\n## Get Started\n\n### Installing\n\nThe easiest way to install `tuify` is via `pip`:\n\n```console\npip install tuify\n```\n\n<!-- TODO: Add optional install for click and other CLIs -->\n\n### Simple Example\n\n## How-to-Guides\n\n## Deep Dive\n\n### Contributing\n\n1. Clone this repository `git clone git@github.com:alwinw/tuify.git`\n2. Install the development version `pip install -v -e .[<extras>]` (`-e` needs pip >= 22.0 for pyproject.toml) or `poetry install --extras "<extras>"`\n3. Make your changes and commit using [commitizen](https://commitizen-tools.github.io/commitizen/#installation) and ensure [pre-commit](https://pre-commit.com/#install) is active\n4. When ready, bump the version and run `poetry build -v`. If deploying, run `poetry publish --build -v`\n\n## Acknowledgements\n\nThis package is heavily inspired by [Gooey](https://github.com/chriskiehl/Gooey) and [Rich CLI](https://github.com/Textualize/rich-cli). It would not be possible without [Textualize](https://github.com/Textualize) and [click](https://github.com/pallets/click)\n',
    'author': 'alwinw',
    'author_email': '16846521+alwinw@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alwinw/tuify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
