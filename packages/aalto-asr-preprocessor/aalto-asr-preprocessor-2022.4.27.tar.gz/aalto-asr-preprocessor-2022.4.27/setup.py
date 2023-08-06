# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aalto_asr_preprocessor',
 'aalto_asr_preprocessor.fi',
 'aalto_asr_preprocessor.fi.numbers']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['aalto-prep = aalto_asr_preprocessor.__main__:main']}

setup_kwargs = {
    'name': 'aalto-asr-preprocessor',
    'version': '2022.4.27',
    'description': 'Aalto ASR preprocessing tool for preparing texts.',
    'long_description': "Aalto ASR preprocessing package\n===============================\n\n|PyPI| |Python Version| |License|\n\n|Tests| |pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/aalto-asr-preprocessor.svg\n   :target: https://pypi.org/project/aalto-asr-preprocessor/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/aalto-asr-preprocessor\n   :target: https://pypi.org/project/aalto-asr-preprocessor\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/aalto-speech/aalto-asr-preprocessor\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Tests| image:: https://github.com/aalto-speech/aalto-asr-preprocessor/workflows/Tests/badge.svg\n   :target: https://github.com/aalto-speech/aalto-asr-preprocessor/actions?workflow=Tests\n   :alt: Tests\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nFeatures\n--------\n\n* Rule-based preprocessing recipes for ASR\n* Recipes are validated with tests\n\nRequirements\n------------\n\n* Python >= 3.8\n* Click\n\nInstallation\n------------\n\nYou can install *aalto-asr-preprocessor* via pip_ from PyPI_:\n\n.. code-block:: console\n\n   $ pip install aalto-asr-preprocessor\n\nUsage\n-----\n\nFor detailed instructions, see `Usage`_\nor type ``aalto-prep --help`` in terminal.\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Aalto ASR preprocessor* is free and open source software.\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\nCredits\n-------\n\nThis project uses `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _MIT: http://opensource.org/licenses/MIT\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/aalto-speech/aalto-asr-preprocessor/issues\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: docs/index.rst\n.. _pip: https://pip.pypa.io/\n.. _PyPI: https://pypi.org/\n",
    'author': 'Anja Virkkunen',
    'author_email': 'anja.virkkunen@aalto.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aalto-speech/aalto-asr-preprocessor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
