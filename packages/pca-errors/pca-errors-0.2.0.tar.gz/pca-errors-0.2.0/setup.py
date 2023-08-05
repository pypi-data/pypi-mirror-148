# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pca', 'pca.packages.errors']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pca-errors',
    'version': '0.2.0',
    'description': 'Declarative, parametrizable & L10n-independent errors for python-clean-architecture.',
    'long_description': '# python-clean-architecture\n\n![GitHub tag](https://img.shields.io/github/v/tag/pcah/pca-errors)\n[![development status](https://img.shields.io/badge/development%20status-alpha-yellow.svg)](https://pypi.org/project/pca-errors/)\n[![supports](https://img.shields.io/pypi/pyversions/pca-errors)](pyproject.toml)\n[![build status](https://img.shields.io/github/workflow/status/pcah/pca-errors/code-quality)](https://github.com/pcah/pca-errors/actions)\n[![codecov](https://codecov.io/gh/pcah/pca-errors/branch/master/graph/badge.svg)](https://codecov.io/gh/pcah/pca-errors)\n\n**pca-errors** is a Python library helping to define declarative, parametrizable & [L10n](https://en.wikipedia.org/wiki/Language_localisation)-independent error classes.\n\n**pca-errors** is a part of the Clean Architecture toolset, developed under [*python-clean-architecture*](https://github.com/pcah/python-clean-architecture) project.\n\n<!-- markdownlint-disable-next-line MD001 -->\n#### Development Status  (Stage 3 - Alpha Status)\n\nFor details, look at our [ROADMAP](https://github.com/pcah/pca-errors/tree/master/ROADMAP.md).\n\n#### Get It Now\n\n```bash\n$ pip install -U pca-errors\n```\n\n#### Quickstart\n\n[TBDL]\n\n#### Documentation\n\nYou can look at our [docs](https://github.com/pcah/pca-errors/tree/master/docs/).\n',
    'author': 'lhaze',
    'author_email': 'github@lhaze.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pcah/pca-errors',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
