# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deluge_card', 'tests']

package_data = \
{'': ['*'],
 'tests': ['fixtures/*',
           'fixtures/DC01/KITS/*',
           'fixtures/DC01/SAMPLES/Artists/A/*',
           'fixtures/DC01/SONGS/*',
           'fixtures/DC01/SYNTHS/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'jinja2==3.0.3',
 'lxml>=4.8.0,<5.0.0',
 'mkdocstrings-python>=0.6.5',
 'pymdown-extensions>=9.4']

extras_require = \
{':extra == "doc"': ['mkdocstrings>=0.18.0'],
 'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.1',
         'mkdocs-include-markdown-plugin>=1.0.0',
         'mkdocs-material>=6.1.7',
         'mkdocs-autorefs>=0.3.1'],
 'test': ['black>=22.3',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'deluge-card',
    'version': '0.2.2',
    'description': 'python api for synthstrom deluge cards from fw3.15+.',
    'long_description': '# deluge-card\n\n\n[![pypi](https://img.shields.io/pypi/v/deluge-card.svg)](https://pypi.org/project/deluge-card/)\n[![python](https://img.shields.io/pypi/pyversions/deluge-card.svg)](https://pypi.org/project/deluge-card/)\n[![Build Status](https://github.com/mupaduw/deluge-card/actions/workflows/dev.yml/badge.svg)](https://github.com/mupaduw/deluge-card/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/mupaduw/deluge-card/branch/main/graphs/badge.svg)](https://codecov.io/github/mupaduw/deluge-card)\n\n\n\npython api for synthstrom deluge cards from fw3.15+\n\n\n* Documentation: <https://mupaduw.github.io/deluge-card>\n* GitHub: <https://github.com/mupaduw/deluge-card>\n* PyPI: <https://pypi.org/project/deluge-card/>\n* Free software: MIT\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Chris Chamberlain',
    'author_email': 'chrisbc@artisan.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mupaduw/deluge-card',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
