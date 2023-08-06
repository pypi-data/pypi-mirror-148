# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vlcsync']

package_data = \
{'': ['*']}

install_requires = \
['cached-property', 'loguru', 'psutil']

entry_points = \
{'console_scripts': ['vlcsync = vlcsync.main:main']}

setup_kwargs = {
    'name': 'vlcsync',
    'version': '0.1.5',
    'description': 'Utility for synchronize multiple instances of VLC. Supports seek, play and pause. ',
    'long_description': 'VLC Sync\n========\n\nUtility for synchronize multiple instances of VLC. Supports seek, play and pause. \nInspired by F1 streams with extra driver tracking data.  \n\n# Run\n\n`Vlc` instances should expose "Remote control interface" on 127.0.0.42 (see [how configure vlc](./docs/vlc_setup.md))\n\n```shell\n\n# Run vlc (should with open --rc-host 127.0.0.42 option) \n$ vlc --rc-host 127.0.0.42 SomeMedia1.mkv &\n$ vlc --rc-host 127.0.0.42 SomeMedia2.mkv &\n$ vlc --rc-host 127.0.0.42 SomeMedia3.mkv &\n\n# vlcsync will find all vlc on 127.0.0.42:* and start syncing \n$ vlcsync\n\nVlcsync started...\nFound instance with pid 3538289 and port 127.0.0.42:34759 State(play_state=playing, seek=10)\nFound instance with pid 3538290 and port 127.0.0.42:38893 State(play_state=playing, seek=10)\nFound instance with pid 3538291 and port 127.0.0.42:45615 State(play_state=playing, seek=10)\n```\n\n## Install\n\n```shell\npip3 install -U vlcsync\n```\n\n## Status \n\nIn development. Tested on Linux, but should also work on Win/macOS.\n\nAny thoughts, ideas and contributions welcome!\n\nRoadmap:\n\n- [ ] Add ability to set static addresses i.e. for remote sync (to external pc/screen)\n- [ ] Add portable `*.exe` build for Windows\n\n## Demo\n\n![](./docs/vlcsync.gif)\n\nEnjoy! 🚀',
    'author': 'mrkeuz',
    'author_email': 'mrkeuz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrkeuz/vlcsync/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
