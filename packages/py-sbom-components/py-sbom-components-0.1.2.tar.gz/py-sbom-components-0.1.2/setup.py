# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycomponents']

package_data = \
{'': ['*']}

install_requires = \
['cyclonedx-python-lib>=2.3.0,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'psutil>=5.9.0,<6.0.0',
 'sh>=1.14.2,<2.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['pycomponents = pycomponents.cli:app']}

setup_kwargs = {
    'name': 'py-sbom-components',
    'version': '0.1.2',
    'description': 'An experimental tool to generate CycloneDX BOM from running Python processes',
    'long_description': "# pycomponents\n\n[![PyPI version](https://badge.fury.io/py/py-sbom-components.svg)](https://badge.fury.io/py/py-sbom-components)\n[![Python CI](https://github.com/ninoseki/pycomponents/actions/workflows/test.yml/badge.svg)](https://github.com/ninoseki/pycomponents/actions/workflows/test.yml)\n\nAn experimental tool to generate CycloneDX SBOM from running Python processes.\n\n## Requirements\n\n- Linux and macOS (not tested with Windows)\n- Python 3.8+ (tested with Python 3.8, 3.9 and 3.10)\n\n## Installation\n\n```bash\npip install py-sbom-components\n```\n\nNote: Initially I planned to publish this tool as `pycomponents`. But it is prohibited by the following restriction.\n\n```\nHTTP Error 400: The name 'pycomponents' is too similar to an existing project. See https://pypi.org/help/#project-name for more information.\n```\n\nThus, I use this a little bit lengthy name.\n\n## Usage\n\n```bash\n$ pycomponents --help\nUsage: pycomponents [OPTIONS]\n\nOptions:\n  --output-format [xml|json]      The output format for your SBOM  [default:\n                                  json]\n  --output-dir TEXT               The output directory  [default: ./]\n  --allow-overwrite / --no-allow-overwrite\n                                  Whether to allow overwriting if the same\n                                  file exists  [default: allow-overwrite]\n  --exclude-pids INTEGER          A list of pids to exclude\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n```\n\n## Example\n\nSee [example](https://github.com/ninoseki/pycomponents/tree/main/example).\n\n## What is the difference from `cyclonedx-bom`?\n\n[cyclonedx-bom](https://github.com/CycloneDX/cyclonedx-python)'s BOM comes from:\n- Python Environment\n- Project's manifest (e.g. Pipfile.lock, poetry.lock or requirements.txt)\n\n`pycomponents` uses a different approach to generate SBOM.\n\n- List up Python processes\n- Inspect site packages used by a Python process\n- Generate SBOM based on site packages\n\nThus `pycomponents` generates half-and-half mixed runtime & static SBOM.\n",
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ninoseki/pycomponents',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
