# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hurocon']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'huawei-lte-api>=1.6.0,<2.0.0',
 'serialix>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['hurocon = hurocon.cli:cli']}

setup_kwargs = {
    'name': 'hurocon',
    'version': '0.1.0',
    'description': 'Command line interface tool for interacting with Huawei LTE routers',
    'long_description': '# Hurocon\nHurocon *(**hu**awei **ro**uter **con**trol)* - command line interface tool for interacting with Huawei LTE routers\n\n\n## Features\n- Device Control\n  - Reboot\n- SMS Control\n  - Send\n\n> **Planned**:  \n> *Device Control* - `Information/Stats`, `Signal Level`, `LED Control`;  \n> *SMS Control* - `List`, `View`;  \n> *Connection Control* - `WiFi Settings/Switches`, `Cellular Settings/Switches`;  \n\n\n## Supported Devices\nFull list of supported devices is available on [this link](https://github.com/Salamek/huawei-lte-api#tested-on).\n\n\n## Installation\nCurrently this tool can only be installed with `pip` on `python` >= 3.7. You can install it from PyPi:\n\n```bash\npip install hurocon\n```\n\nOr directly from this Github repo:\n\n```bash\npip install git+https://github.com/maximilionus/hurocon.git\n```\n\n> Built executable mode *([pyinstaller](https://pyinstaller.org/)-based)* is planned but no ETA yet\n\n\n## Quickstart\n### Intro\nAfter successful [installation](#installation) of this tool it can be accessed in shell using the following commands:\n\n```bash\n$ hurocon\n# OR\n$ python -m hurocon\n```\n\nYou can also view a list of all root commands with:\n```bash\n$ hurocon --help\n```\n\nEach command in this tool has a special `--help` flag to display detailed information about it\n\n### Authentification\nFirst of all, you need to specify the authorization and connection data so that this tool can access the router in the future. You do it in two ways.\n\n- In interactive mode:\n  ``` bash\n  $ hurocon auth login\n  ```\n\n- Manually, by running:\n  ```bash\n  # Initialize local configuration file\n  $ hurocon config init\n\n  # Show path to local configuration file\n  $ hurocon config path\n  ```\n\n  And then manually editing the `json` file with any text editor. It has a human-readable structure, so every part of it is exactly what you think it is.\n\n### Testing Connection\nAfter auth details successfully specified you can test your connection with router by running\n\n```bash\n$ hurocon auth test\n\n# Returns\n# Success: Successful Authentification\n# Failure: Auth failed, reason: "..."\n```\n\n### Conclusion\nThat\'s it, you\'re ready to go. And remember - no matter how deep you go, `--help` flag is always here to help 👍\n\n\n## Special\nBig thanks to [Adam Schubert](https://github.com/Salamek) for his amazing [`huawei-lte-api`](https://github.com/Salamek/huawei-lte-api) package, that made this whole thing possible.\n',
    'author': 'maximilionus',
    'author_email': 'maximilionuss@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maximilionus/hurocon.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
