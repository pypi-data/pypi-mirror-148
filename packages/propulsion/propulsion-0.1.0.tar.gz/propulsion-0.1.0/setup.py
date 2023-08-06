# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['propulsion']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'propulsion',
    'version': '0.1.0',
    'description': 'propulsion',
    'long_description': '# Propulsion\n\n:warning: _This package is currently under development_\n\n## Get Started\n\n### Installing\n\nThe easiest way to install `propulsion` is via `pip`:\n\n```console\npip install propulsion\n```\n\n<!-- TODO: Add optional install for click and other CLIs -->\n\n### Simple Example\n\n## How-to-Guides\n\n## Deep Dive\n\n### Contributing\n\n1. Clone this repository `git clone git@github.com:alwinw/propulsion.git`\n2. Install the development version `pip install -v -e .[<extras>]` (`-e` needs pip >= 22.0 for pyproject.toml) or `poetry install --extras "<extras>"`\n3. Make your changes and commit using [commitizen](https://commitizen-tools.github.io/commitizen/#installation) and ensure [pre-commit](https://pre-commit.com/#install) is active\n4. When ready, bump the version and run `poetry build -v`. If deploying, run `poetry publish --build -v`\n\n## Acknowledgements\n\nThis package is heavily inspired by [Gooey](https://github.com/chriskiehl/Gooey) and [Rich CLI](https://github.com/Textualize/rich-cli). It would not be possible without [Textualize](https://github.com/Textualize) and [click](https://github.com/pallets/click)\n',
    'author': 'alwinw',
    'author_email': '16846521+alwinw@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
