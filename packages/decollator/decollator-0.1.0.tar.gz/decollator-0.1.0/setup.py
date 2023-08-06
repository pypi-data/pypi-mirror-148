# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['decollator']

package_data = \
{'': ['*']}

install_requires = \
['tomli-w>=1.0.0,<2.0.0', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['prysk = decollator:cli.main']}

setup_kwargs = {
    'name': 'decollator',
    'version': '0.1.0',
    'description': 'changelog & stuff',
    'long_description': 'decollator\n=================================\n\n\n\n\n\n\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n\n.. image:: https://img.shields.io/badge/imports-isort-ef8336.svg\n    :target: https://pycqa.github.io/isort/\n\n.. image:: https://img.shields.io/badge/docs-available-blue.svg\n    :target: https://nicoretti.github.io/decollator/\n\n.. image:: https://img.shields.io/badge/pypi%20package-unavailable-red.svg\n     :target: https://pypi.org/project/decollator/\n     :alt: PyPI Version\n\n\nGetting Started\n+++++++++++++++\n\n#. Setup virtual environment for development\n\n    .. code-block:: shell\n\n        poetry shell\n\n#. Install a dependencies\n\n    .. code-block:: shell\n\n        poetry install\n\n#. List all tasks/targets\n\n    .. code-block:: shell\n\n        nox -l\n\n',
    'author': 'Nicola Coretti',
    'author_email': 'nico.coretti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicoretti/decollator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
