# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hathorlib', 'hathorlib.conf']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.0', 'cryptography>=3.3.1']

extras_require = \
{'client': ['structlog>=20.0.0', 'aiohttp>=3.7.0']}

setup_kwargs = {
    'name': 'hathorlib',
    'version': '0.2.0',
    'description': 'Hathor Network base objects library',
    'long_description': "hathorlib\n=========\n\nHathor Network base library.\n\n## Configuration\n\nTo install dependencies, including optionals, run:\n\n    poetry install -E client\n\n## Running the tests\n\nTo run the tests using poetry virtualenv:\n\n    poetry run make tests\n\nIf are managing virtualenvs without poetry, make sure it's activated and run:\n\n    make tests\n\n## Running linters\n\nTo run linters:\n\n    poetry run make check\n\nOr without poetry venv:\n\n    make check",
    'author': 'Hathor Team',
    'author_email': 'contact@hathor.network',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hathor.network/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
