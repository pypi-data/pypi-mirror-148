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
    'version': '0.1.0',
    'description': 'An experimental tool to generate CycloneDX SBOM from running Python processes',
    'long_description': None,
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
