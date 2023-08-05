# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'thermal', 'thermal.sample', 'thermal.stats']

package_data = \
{'': ['*']}

install_requires = \
['click==8.0.4',
 'myst-parser>=0.17.2,<0.18.0',
 'numpy>=1.22.3,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'sklearn>=0.0,<0.1']

extras_require = \
{':extra == "docs"': ['Sphinx>=4.5.0,<5.0.0',
                      'sphinx-rtd-theme>=1.0.0,<2.0.0',
                      'nbsphinx>=0.8.8,<0.9.0'],
 ':extra == "test"': ['black>=22.3.0,<23.0.0'],
 'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'test': ['isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

entry_points = \
{'console_scripts': ['thermal = thermal.cli:main']}

setup_kwargs = {
    'name': 'thermal',
    'version': '0.6.3',
    'description': 'Surrogate times eries generation.',
    'long_description': '# thermal\n\n[![pypi](https://img.shields.io/pypi/v/thermal.svg)](https://pypi.org/project/thermal/)\n[![python](https://img.shields.io/pypi/pyversions/thermal.svg)](https://pypi.org/project/thermal/)\n[![Build Status](https://github.com/sitmo/thermal/actions/workflows/dev.yml/badge.svg)](https://github.com/sitmo/thermal/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/sitmo/thermal/branch/main/graphs/badge.svg)](https://codecov.io/github/sitmo/thermal)\n\nModel Free surrogate time series generation.\n\n\n\n\n\n* Documentation: <https://sitmo.github.io/thermal>\n* GitHub: <https://github.com/sitmo/thermal>\n* PyPI: <https://pypi.org/project/thermal/>\n* Free software: MIT\n\n\n## Features\n\n* TODO\n',
    'author': 'Thijs van den Berg',
    'author_email': 'thijs@sitmo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sitmo/thermal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
