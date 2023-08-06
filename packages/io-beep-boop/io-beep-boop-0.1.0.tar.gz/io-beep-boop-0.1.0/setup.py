# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['io_beep_boop', 'io_beep_boop.api', 'io_beep_boop.cli', 'io_beep_boop.tests']

package_data = \
{'': ['*']}

install_requires = \
['cfig[cli]>=0.2.3,<0.3.0',
 'click>=8.1.2,<9.0.0',
 'httpx>=0.22.0,<0.23.0',
 'pydantic>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['io-beep-boop = io_beep_boop.cli.__main__:main']}

setup_kwargs = {
    'name': 'io-beep-boop',
    'version': '0.1.0',
    'description': '',
    'long_description': '# `io-beep-boop`\n\nAn experimental wrapper and command line interface for the Italian [IO App API](https://developer.io.italia.it/openapi.html)\n\n\\[ [**Documentation**](https://io-beep-boop.readthedocs.io/en/latest/index.html) | [**PyPI**](https://pypi.org/project/io-beep-boop/) \\]\n\n```console\n$ io-beep-boop\nUsage: io-beep-boop [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version         Show the version and exit.\n  -t, --token TEXT  One of the two IO App API tokens of the service you want\n                    to use.\n  --base-url TEXT   The base URL of the IO App API to use.\n  --help            Show this message and exit.\n\nCommands:\n  registered-fast\n  registered-slow\n  ...\n```\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'you@example.org',
    'maintainer': 'Stefano Pigozzi',
    'maintainer_email': 'you@example.org',
    'url': 'https://github.com/Steffo99/io-beep-boop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
