# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nettowel', 'nettowel.cli']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.20.0,<0.21.0',
 'qrcode>=7.3.1,<8.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.0.1,<13.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'typer>=0.4.1,<0.5.0']

extras_require = \
{'full': ['Jinja2>=3.0.3,<4.0.0',
          'ttp>=0.8.4,<0.9.0',
          'textfsm>=1.1.2,<2.0.0',
          'napalm>=3,<4',
          'netmiko>=4,<5',
          'scrapli>=2022.1.30,<2023.0.0',
          'nornir>=3.2.0,<4.0.0'],
 'jinja': ['Jinja2>=3.0.3,<4.0.0', 'jinja2schema>=0.1.4,<0.2.0'],
 'napalm': ['napalm>=3,<4'],
 'netmiko': ['netmiko>=4,<5'],
 'nornir': ['nornir>=3.2.0,<4.0.0'],
 'scrapli': ['scrapli>=2022.1.30,<2023.0.0'],
 'textfsm': ['textfsm>=1.1.2,<2.0.0'],
 'ttp': ['ttp>=0.8.4,<0.9.0']}

entry_points = \
{'console_scripts': ['nettowel = nettowel.cli.main:run',
                     'nt = nettowel.cli.main:run']}

setup_kwargs = {
    'name': 'nettowel',
    'version': '0.3.0',
    'description': 'Network Automation Collection',
    'long_description': '# nettowel\nCollection of useful network automation functions \n\n> ⚠️ `nettowel` is under heavy construction and not production ready. Feedback is highly appreciated.\n\n\n## Install\n\nYou can install `nettowel` directly from pypi\n\n```bash\npip install nettowel\n```\n\nTo reduce the dependencies the extra dependencies are grouped\n\nThe following groups are available (more details in the in the pyproject.toml):\n\n- full\n- jinja\n- ttp\n- textfsm\n- napalm\n- netmiko\n- scrapli\n- nornir\n\n```bash\npip install nettowel[jinja]\npip install nettowel[full]\n```\n\n## Install from source\n\n```\ngit clone ....\ncd nettowel\npoetry install\npoetry run nettowel --help\n```\n\n\n## Help and shell auto completion\n\nThanks to the library [typer](https://typer.tiangolo.com/) `nettowel` comes with a nice help and autocompletion install\n\n![help](imgs/help.png)\n\n\n## Features\n\nMany features are not implemented yet and many features will come.\n\n\n\n### Jinja2\n\n#### render\n\n![jinja rendering 1](imgs/jinja-render-3.png)\n\n![jinja rendering 2](imgs/jinja-render-1.png)\n\n#### validate\n\n![jinja validate](imgs/jinja-validate.png)\n\n#### variables\n\n![jinja variables](imgs/jinja-variables.png)\n\n\n### TTP\n\n#### render\n\n![ttp render](imgs/ttp-render.png)\n\n### Netmiko\n\n#### cli\n\n![netmiko cli](imgs/netmiko-cli.png)\n\n#### autodetect\n\n![netmiko autodetect](imgs/netmiko-autodetect.png)\n\n#### device-types\n\n![netmiko device types](imgs/netmiko-device-types.png)\n\n\n### RESTCONF\n\n#### get\n\n![restconf get](imgs/restconf-get.png)\n\n#### patch, delete\n\n![restconf patch delete](imgs/restconf-patch-delete.png)\n\n#### post, put\n\n![restconf post put](imgs/restconf-post-put.png)\n\n### ipaddress\n\n#### ip-info\n\n![ip info](imgs/ip-info.png)\n\n#### network-info\n\n![network info](imgs/network-info.png)\n\n\n### Help\n\n![Help QRcode](imgs/nettowel-help.png)\n\n\n### Settings\n\nA `dotenv` file can be used as a settings file. It also be provided an `dotenv` file with the option `--dotenv`.\n\n![environment settings](imgs/env-settings.png)\n\n\n### Piping\n\n![piping](imgs/piping.png)\n\n\n\n## Building CLI Docs\n\n**At the moment `typer-cli` is not ready for typer 0.4.0**\n\n```\ntyper nettowel/cli/main.py utils docs --name nettowel --output CLI.md\n```\n',
    'author': 'ubaumann',
    'author_email': 'github@m.ubaumann.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/InfrastructureAsCode-ch/nettowel/tree',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
