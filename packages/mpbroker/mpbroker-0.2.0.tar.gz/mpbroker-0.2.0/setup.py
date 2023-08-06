# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpbroker', 'mpbroker.config', 'mpbroker.models']

package_data = \
{'': ['*'], 'mpbroker': ['example/*']}

install_requires = \
['arrow>=1.2.2,<2.0.0',
 'pycouchdb>=1.14.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.3.0,<13.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['mpb = mpbroker.main:app']}

setup_kwargs = {
    'name': 'mpbroker',
    'version': '0.2.0',
    'description': 'Media Player Broker',
    'long_description': '# README\n\n**NOTICE: this is a beta release, expect things to change (and soon)!**\n\nMedia Player Broker (mpb) is an application that helps you play and track media you have watched over disparet locations. mpb keeps track of what you have played at Location A so when you are at Location B you can see what you have watched from either location to avoid digging through history command output over SSH. mpb is not a player itself, it can be configured to launch a player such as vlc, smplayer or others when you use the \'play\' command.\n\n\n### The Need\n\nI needed something that remembers what episode of MacGyver I had watched in one location so when I was in another location I could continue watching the next episode without digging through `history` output or keeping track of what was played where.\n\nmpb consists of a CLI application (the client) and a database (couchdb). From the client you `injest` your media metadata. This extracts the file names from file paths and stores the data in the database. After injesting, you can `list` your media which shows you the media Item, whether it has been watched or not along with a Rating, Notes, and the Sources the item is available at. You can then use the `play` command along with the Item to watch the Item. After playback is completed you are prompted to mark the item as played/watched, Rate it and add Notes - all of which are used in the `list` command to show what you have already watched and what is new.\n\n\n###  Setup  ###\n\nThe following steps use a virtual environment for the application (which is recommended) but not required:\n\nNote: APP_ROOT is the directory that contains the `main.py` file\n\n- add a python virtual environment and activate:\n  - in APP_ROOT; create virtualenv: `python3 -m virtualenv .venv`\n  - in APP_ROOT; activate virtualenv: `source .venv/bin/activate`\n- install requirements:\n  - in APP_ROOT; install requirements `pip install -r requirements.txt`\n  - deactivate virtualenv as you should no longer need it: `deactivate`\n- create app symlink:\n  - in APP_ROOT; `ln -sf -T "$(pwd)/bin/mpb" "$HOME/bin/mpb"`\n  - note: you may want the link in something other than `$HOME/bin/mpb`, we recommend this directory if it is in your PATH, otherwise add it to PATH or adjust the symlink to wherever you need it (e.g. `/usr/local/bin`, etc.)\n\n\n### Configure\n\nNOTICE:\n - an example `user_config.toml` file can be found in the `client/example` directory\n - if you do not want to use the standard locations and do not want to set a MPB_CONFIG_HOME envvar you can set MPB_CONFIG_HOME on the command line before calling mpb such as `MPB_CONFIG_HOME=/opt/tmp ./main.py list \'The_Matrix\'`)\n\nTo set up MBP you need to:\n- create your `user_config.toml` file and place it in one of the following locations :\n  + MPB_CONFIG_HOME\n  + XDG_CONFIG_HOME/mpb\n  + APPDATA/mpb\n  + HOME/.config/mpb\n- configure your user_config.toml file as needed\n- ensure your mpb database is available\n  + use the `db-init` command to initialize your db if it is a new instance!\n',
    'author': 'David Rader',
    'author_email': 'sa@adercon.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
