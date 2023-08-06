# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_prefer_nested_dup_tests']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.1,<8.0.0']

entry_points = \
{'pytest11': ['prefer-nested-dup-tests = pytest_prefer_nested_dup_tests']}

setup_kwargs = {
    'name': 'pytest-prefer-nested-dup-tests',
    'version': '0.1.0',
    'description': 'A Pytest plugin to drop duplicated tests during collection, but will prefer keeping nested packages.',
    'long_description': 'pytest-prefer-nested-dup-tests\n==============================\n\nby Marximus Maximus (https://www.marximus.com)\n\n.. image:: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/workflows/main/badge.svg\n  :target: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/actions\n  :alt: Test Status\n  :align: center\n\n.. TODO: coveralls.io\n.. .. image:: https://coveralls.io/repos/github/MarximusMaximus/pytest-prefer-nested-dup-tests/badge.svg?branch=main\n..    :target: https://coveralls.io/github/MarximusMaximus/pytest-prefer-nested-dup-tests?branch=main\n..    :alt: Coverage Status\n..    :align: center\n..\n.. TODO: readthedocs.org\n.. .. image:: https://readthedocs.org/projects/pytest-prefer-nested-dup-tests/badge/?version=stable\n..    :target: https://pytest-prefer-nested-dup-tests.readthedocs.io/en/stable/?badge=stable\n..    :alt: Documentation Status\n..    :align: center\n..\n.. TODO: readthedocs.org license\n.. .. image:: https://pytest-prefer-nested-dup-tests.readthedocs.io/en/stable/_static/license.svg\n..    :target: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/blob/main/LICENSE\n..    :alt: License: MIT\n..    :align: center\n..    :align: center\n..\n.. image:: http://img.shields.io/pypi/v/pytest-prefer-nested-dup-tests.svg\n   :target: https://pypi.python.org/pypi/pytest-prefer-nested-dup-tests\n   :alt: PyPI Version\n   :align: center\n\n.. image:: https://pepy.tech/badge/pytest-prefer-nested-dup-tests\n   :target: https://pepy.tech/project/pytest-prefer-nested-dup-tests\n   :alt: Downloads\n   :align: center\n.. TODO: conda-forge\n.. .. image:: https://img.shields.io/conda/dn/conda-forge/pytest-prefer-nested-dup-tests.svg?label=conda-forge\n..    :target: https://anaconda.org/conda-forge/pytest-prefer-nested-dup-tests/\n..    :alt: conda-forge\n..\n\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n   :align: center\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Code style: black\n   :align: center\n.. TODO: #8 (add additional linter? isort)\n.. .. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n..    :target: https://pycqa.github.io/isort/\n..    :alt: Uses isort\n..    :align: center\n\nA Pytest plugin to drop duplicated tests during collection, but will prefer keeping nested packages.\n\nBy default, when de-duplicating tests, all sub-packages become top level packages. This plugin keeps\nthe subpackage structure intact.\n\n\nInstallation\n------------\n\nYou can install via `pip`_ from `PyPI`_::\n\n    $ pip install pytest-prefer-nested-dup-tests\n\n\nUsage\n-----\n\nThe plugin is enabled by default, no other action is necessary.\n\n\nContributing\n------------\n\nContributions are very welcome. Please see `CONTRIBUTING.rst`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT`_ license, "pytest-prefer-nested-dup-tests" is free and open source software.\n\nLicense file is available at `LICENSE`_ in "plaintext" (ASCII (ASCII-7), Extended ASCII (ASCII-8), Latin-1,\nWindows-1252, and UTF-8 compatible format).\n\n\nIssues\n------\n\nIf you encounter any problems, please `file an issue`_ along with a detailed description.\n\n\nChangelog\n---------\n\nPlease see `CHANGELOG.rst`_.\n\n\nLike My Work & Want To Support It?\n----------------------------------\n\n- Main Website: https://www.marximus.com\n- Patreon (On Going Support): https://www.patreon.com/marximus\n- Ko-fi (One Time Tip): https://ko-fi.com/marximusmaximus\n\n\n.. _`CHANGELOG.rst`: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/blob/main/CHANGELOG.rst\n.. _`CONTRIBUTING.rst`: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/blob/main/CONTRIBUTING.rst\n.. _`file an issue`: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/issues\n.. _`LICENSE`: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/blob/main/LICENSE\n.. _`MIT`: http://opensource.org/licenses/MIT\n.. _`pip`: https://pypi.python.org/pypi/pip/\n.. _`PyPI`: https://pypi.python.org/pypi\n',
    'author': 'Marximus Maximus',
    'author_email': 'marximus@marximus.com',
    'maintainer': 'Marximus Maximus',
    'maintainer_email': 'marximus@marximus.com',
    'url': 'https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
