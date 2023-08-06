# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptik', 'cryptik.config']

package_data = \
{'': ['*']}

install_requires = \
['arrow==1.2.2', 'click==8.1.3', 'toml==0.10.2', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['cryptik = cryptik.main:app']}

setup_kwargs = {
    'name': 'cryptik',
    'version': '3.8.0',
    'description': 'display cryptocurrency prices',
    'long_description': '## About ##\n\na [cli](https://en.wikipedia.org/wiki/Command-line_interface)-based application for displaying the current price of a cryptocurrency. cryptik supports multiple exchanges and multiple currencies.\n\nPlease see the project wiki for supported currencies and supported exchanges or to request new currencies/exchanges.\n\n\n## Requirements ##\n\n- python3\n\n\n## Install\n\n- download cryptik: \n\n```\n# set release tag as desired.\nrelease=3.1.1\nwget https://gitlab.com/drad/cryptik/-/archive/${release}/cryptik-${release}.tar.bz2 \\\n  && tar -xjf cryptik-${release}.tar.bz2 \\\n  && rm cryptik-${release}.tar.bz2 \\\n  && chmod u+x cryptik-${release}/cryptik.py\n```\n\n\n## Setup ##\n\nAlthough a virtual environment is not required, we strongly recommend it to keep cryptic\'s requirements separated from other python apps you may have. You can create a virtual environment with the following: \n\n- install virtualenv: `pacman -S virtualenv`\n- setup virtualenv for cryptic (in cryptic root): `python3 -m virtualenv .venv`\n- activate virtualenv: `source .venv/bin/activate`\n- install requirements: `pip install -r requirements.txt`\n\nWe recommend copying the config file to `~/.config/cryptik`:\n```\nmkdir ~/.config/cryptik \\\n  && cp cryptik-${release}/example/config.toml ~/.config/cryptik/\n```\n> ignore this step if you already have a `config.toml` file setup\n\n- modify the config file as needed\n\t- note: no changes are required; however, the app can be customized to your taste.\n- create app symlink (optional): `ln -sf -t ~/bin/ "$HOME/apps/cryptik/cryptik-${release}/cryptik.py"`\n  - note: replace ${release} with the version you downloaded\n  - note: the above symlink assumes you perform the download step (above) in the ~/apps/cryptik directory and that ~/bin is in your $PATH\n\n\n## Usage ##\n- call cryptik from command line: `cryptik.py -e BITSTAMP -t BTC`\n\t- show full response: `cryptik.py -d full`\n- list all available exchanges: `cryptik.py -l`\n- get help on cryptik: `cryptik.py -h`\n- example conky usage (note: this will show prices from two exchanges):\n```\nCRYPTIK\n  ${texeci 600 cryptik.py -e KRAKEN -t BTC}\n  ${texeci 600 cryptik.py -e BITSTAMP -t BTC}\n```\n\n## Example Response\n* direct call:\n```\n$ cryptik.py -e BITSTAMP -t BTC\nBTMP:BTC $9711.24 @12:33\n```\n',
    'author': 'David Rader',
    'author_email': 'sa@adercon.com',
    'maintainer': 'David Rader',
    'maintainer_email': 'sa@adercon.com',
    'url': 'https://gitlab.com/drad/cryptik',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
