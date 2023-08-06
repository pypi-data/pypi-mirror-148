# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_commit_license_headers']

package_data = \
{'': ['*']}

install_requires = \
['identify>=2.2.13,<3.0.0']

entry_points = \
{'console_scripts': ['check-license-headers = '
                     'pre_commit_license_headers.check_license_headers:main']}

setup_kwargs = {
    'name': 'pre-commit-license-headers',
    'version': '0.1.0',
    'description': 'A pre-commit hook to check source code license headers',
    'long_description': '# Pre-Commit License Headers\n\nA [pre-commit](https://github.com/pre-commit/pre-commit) hook to check the license\nheaders of your source code files.\n\nAt present, it only supports checking files that use hash mark `#` comment syntax. For\nmore info, see [Supported file types](#supported-file-types).\n\n### Usage\n\nAdd an entry like this to your `.pre-commit-config.yaml`\n\n```yaml\n- repo: https://github.com/johannsdg/pre-commit-license-headers\n  rev: v0.1.0 # Use the ref you want to point at\n  hooks:\n    - id: check-license-headers\n      args:\n        - "--template"\n        - |\n          Copyright (c) [YEARS] [OWNER]\n          Use of this source code is governed by a BSD-3-clause license that can\n          be found in the LICENSE file or at https://opensource.org/licenses/BSD-3-Clause\n        - "--owner=The Pre-Commit License Headers Authors"\n```\n\n(Note that the template provided above is the default, so if you are using BSD-3-clause\nand are happy with the wording, you can skip `--template` and just provide `--owner`)\n\n`[YEARS]` and `[OWNER]` are optional variables in the header template. If used, they\nwill automatically be replaced with:\n\n- `[YEARS]`: a regular expression that accepts various combinations of years, such as:\n  - Single years, such as \'2019\' or \'2021\'\n  - Year ranges, such as \'2018-2020\'\n  - Combinations, such as \'2014, 2016-2018, 2020\'\n  - Note that ranges ending in \'-present\' are not supported\n- `[OWNER]`: the contents of the `--owner` argument\n  - Note that `--owner` is optional unless the template uses the `[OWNER]` variable\n\n### Supported file types\n\n`Pre-Commit License Headers` supports checking file types that use hash mark `#` comment\nsyntax.\n\nThis includes:\n\n- python\n- shell\n- yaml\n- toml\n- plain-text\n- etc\n\nFor the list of file types checked by default, see\n[file_types.py](pre_commit_license_headers/file_types.py) You may override the default\nlist with your own via the `-f` or `--file-type` option (may be specified multiple\ntimes).\n\nFile types are determined using the [identify](https://github.com/pre-commit/identify)\nlibrary. For more information about file types, see:\nhttps://pre-commit.com/#filtering-files-with-types\n\n### As a standalone package\n\n`Pre-Commit License Headers` is also available as a standalone package.\n\nTo install via pip:\n\n`pip install pre-commit-license-headers`\n\nYou may also clone this repo and install via [poetry](https://python-poetry.org/):\n\n`poetry install --no-dev`\n\nEither installation option will place the `check-license-headers` executable in your\nenvironment\'s configured binary directory (e.g., \'.venv/bin\')\n\nTo use:\n\n```console\nfoo@bar:~$ check-license-headers --help\nusage: check-license-headers [-h] [-d] [--list-file-types] [-s] [-f FILE_TYPE]\n                             [-o COPYRIGHT_OWNER] -t TEMPLATE\n                             [FILE [FILE ...]]\n\nChecks if file headers match a provided template.\n\npositional arguments:\n  FILE\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -d, --debug\n  --list-file-types     lists all text file types and exits\n  -s, --summary         prints a summary after checking the files\n  -f FILE_TYPE, --file-type FILE_TYPE\n                        may be specified multiple times\n  -o COPYRIGHT_OWNER, --owner COPYRIGHT_OWNER\n  -t TEMPLATE, --template TEMPLATE\n```\n',
    'author': 'Jeffrey James',
    'author_email': 'lobotmcj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johannsdg/pre-commit-license-headers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
