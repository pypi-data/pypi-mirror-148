# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jumparound']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click>=8.0.3,<9.0.0', 'textual>=0.1.12,<0.2.0']

entry_points = \
{'console_scripts': ['jumparound = jumparound.cli:cli']}

setup_kwargs = {
    'name': 'jumparound',
    'version': '1.0.0',
    'description': 'Quickly jump around between your projects.',
    'long_description': '# jumparound\n\nQuickly jump around between your projects.\n\n## Installation\n\n```\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\npython3 -m pipx install jumparound\n```\n\n## Usage\n\n`jumparound` can be used on its own or as a part of other scripts. The most common usage is in\nconjunction with `cd`.\n\n```sh\ncd $("jumparound to")\n```\n\n## Development\n\n### Setup\n\n* Have python `poetry` installed.\n* Clone this repository.\n* Run `make setup`\n',
    'author': 'Matt Porter',
    'author_email': 'mtp5129@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/M-Porter/jumparound',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
