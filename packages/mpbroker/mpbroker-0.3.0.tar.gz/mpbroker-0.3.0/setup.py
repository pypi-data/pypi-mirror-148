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
    'version': '0.3.0',
    'description': 'Media Player Broker',
    'long_description': "# README\n\n**NOTICE: this app is being released in beta status, things will likely change but we will do our best to make non-breaking changes.**\n\nMedia Player Broker (mpb) is an application that helps you play and track media you have watched over disparet locations. mpb keeps track of what you have played at Location A so when you are at Location B you can see what you have watched from either location to avoid digging through history command output over SSH. mpb is not a player itself, it can be configured to launch a player such as vlc, smplayer or others when you use the 'play' command.\n\n\n### The Need\n\nI needed something that remembers what episode of MacGyver I had watched in one location so when I was in another location I could continue watching the next episode without digging through `history` output or keeping track of what was played where.\n\nmpb consists of a CLI application (the client) and a database (couchdb). From the client you `injest` your media metadata. This extracts the file names from file paths and stores the data in the database. After injesting, you can `list` your media which shows you the media Item, whether it has been watched or not along with a Rating, Notes, and the Sources the item is available at. You can then use the `play` command along with the Item to watch the Item. After playback is completed you are prompted to mark the item as played/watched, Rate it and add Notes - all of which are used in the `list` command to show what you have already watched and what is new.\n\n\n### Install\n\nWe recommend using [pipx](https://github.com/pypa/pipx) to install mpbroker: `pipx install mpbroker`. You can also install via pip: `pip install --user mpbroker`.\n\nmpbroker uses a config file to store your setup. This file contains information such as your media player, the database url, and types of data to injest. You can grap the sample config file at `mpbroker/example/user_config.toml` and place it in a config location. mpbroker searches the following locations for the config file in order of preference:\n\n- $MPB_CONFIG_HOME: set this environment variable to any path you like and place the mpbroker `user_config.toml` file in this location\n- $XDG_CONFIG_HOME/mpbroker\n- $APPDATA/mpbroker\n- $HOME/.config/mpbroker\n\n\n### Configure\n\nNOTICE:\n - an example `user_config.toml` file can be found in the `mpbroker/example` directory\n - if you do not want to use the standard locations and do not want to set a MPB_CONFIG_HOME envvar you can set MPB_CONFIG_HOME on the command line before calling mpb such as `MPB_CONFIG_HOME=/opt/tmp mpb list 'The_Matrix'`)\n\nTo set up MBP you need to:\n- create your `user_config.toml` file (see above for locations of this file)\n- configure your user_config.toml file (at a minimum you will need to set/change the `database.db_uri` value)\n- ensure your mpb database is available\n  + use the `db-init` command to initialize your db if it is a new instance!\n\nIf you are testing mpb or do not have a database you can use docker-compose to start a local database: `docker-compose up`. If you use the local database your `database.db_uri` should be `http://admin:couchdb@localhost:5984`.\n\n\n### Using mpb\n\nmpb has built in help (`mpb --help`) which should give you enough info to get going.\n\nA Quick Start:\n\n- you will likely want to `injest` some media\n- next you can use `list` to view/find an item to play\n- finally you can `play` an item\n\n",
    'author': 'David Rader',
    'author_email': 'sa@adercon.com',
    'maintainer': 'David Rader',
    'maintainer_email': 'sa@adercon.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
