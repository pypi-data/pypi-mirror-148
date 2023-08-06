# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_multi_theme']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.0.0', 'funcy', 'seedir']

extras_require = \
{':python_version < "3.7"': ['dataclasses']}

setup_kwargs = {
    'name': 'sphinx-multi-theme',
    'version': '1.0.0',
    'description': 'A Sphinx extension that builds copies of your docs using multiple themes into separate subdirectories.',
    'long_description': '# sphinx-multi-theme\n\n[![Github-CI][github-ci]][github-link]\n[![Coverage Status][codecov-badge]][codecov-link]\n[![Documentation Status][rtd-badge]][rtd-link]\n[![Code style: black][black-badge]][black-link]\n[![PyPI][pypi-badge]][pypi-link]\n\n[github-ci]: https://github.com/Robpol86/sphinx-multi-theme/actions/workflows/ci.yml/badge.svg?branch=main\n[github-link]: https://github.com/Robpol86/sphinx-multi-theme/actions/workflows/ci.yml\n[codecov-badge]: https://codecov.io/gh/Robpol86/sphinx-multi-theme/branch/main/graph/badge.svg\n[codecov-link]: https://codecov.io/gh/Robpol86/sphinx-multi-theme\n[rtd-badge]: https://readthedocs.org/projects/sphinx-multi-theme/badge/?version=latest\n[rtd-link]: https://sphinx-multi-theme.readthedocs.io/en/latest/?badge=latest\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black-link]: https://github.com/ambv/black\n[pypi-badge]: https://img.shields.io/pypi/v/sphinx-multi-theme.svg\n[pypi-link]: https://pypi.org/project/sphinx-multi-theme\n\nA Sphinx extension that builds copies of your docs using multiple themes into separate subdirectories.\n\n📖 See the documentation at https://sphinx-multi-theme.readthedocs.io\n\n## Install\n\nRequires Python 3.6 or greater and Sphinx 4.0 or greater. Not supported on Windows.\n\n```shell\npip install sphinx-multi-theme\n```\n\n## Example\n\n```python\n# conf.py\nfrom sphinx_multi_theme.theme import MultiTheme, Theme\n\nextensions = [\n    "sphinx_multi_theme.multi_theme",\n]\n\nhtml_theme = MultiTheme(\n    [\n        Theme("sphinx_rtd_theme", "Read the Docs"),\n        Theme("alabaster", "Alabaster"),\n        Theme("classic", "Classic"),\n    ]\n)\n```\n\n```rst\n===============\nAn RST Document\n===============\n\n.. multi-theme-toctree::\n    :caption: Example Themes\n\n```\n',
    'author': 'Robpol86',
    'author_email': 'robpol86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
