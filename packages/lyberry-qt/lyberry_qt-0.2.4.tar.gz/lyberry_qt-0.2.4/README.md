# LyBerry

A Qt LBRY client that uses the LyBerry Api

## Status

You can't do everything you can do in LBRY Desktop, but many essential features are in place:

- Following Feed
- Watch Videos (in configurable external video player)
- Read Articles
- Read / Write / Reply to Comments (on configurable comment server)
- Basic search

## Installation

First [install a recent version of Python 3](https://www.python.org/downloads/).

Then install the package with pip:

```
pip install lyberry-qt
```

Get more info from Python about installing packages:
<https://packaging.python.org/en/latest/tutorials/installing-packages/>

## Usage

Run the app:

```
lyberry-qt
```

LyBerry depends on the lbrynet daemon. This is provided by [the official LBRY Desktop application](https://lbry.com/get), so if that is open in the background LyBerry should just work, and will share the logged in accounts.

You can instead run the daemon alone; get more info about that here: <https://github.com/lbryio/lbry-sdk#installation>. LyBerry is designed to work with the daemon over the network, so you could leave this running on a homeserver for good uptime seeding content. (Note: Don't expose the lbrynet api to the open Internet!)

Videos will try to open in [mpv](https://mpv.io) by default. This option can be changed with the `player_cmd` setting, found on the settings page. On windows, you will want to change `mpv` to `mpv.exe`. You could also use VLC, or another video player if you wish.

You can also change settings in conf.toml in your relevant config directory. (eg on linux edit ~/.config/lyberry/conf.toml)

If some thumbnails are not showing you may need to install a Qt image format library on your system. Search for this using your package manager.

## Help

Join my space on matrix! I am happy to help you getting started, and I welcome feedback and discussion.

LyBerry Matrix channel: [#lyberry:thebeanbakery.xyz](https://matrix.to/#/#lyberry:thebeanbakery.xyz)

## Contributing

Sharing my project is the best way to support it! If you can contribute code too, that would be awesome!
Read CONTRIBUTING.md for more info on getting set up. Do join my matrix room too.

Otherwise, I would greatly appreciate any donations with Monero (XMR), a secure and private currency for the internet:

openalias: thebeanbakery.xyz

87uvs847voZW4QzLqCb3prfSeTjVgxo8PKCAGmeYQTKYd58yU7FD9PJY2eoDXW7y4jNozfHW3bq6SC6MZaB6Qgcz9Cib1DS

You can also support my channel on LBRY, where I sometimes post updates: <lbry://@MyBeansAreBaked:b>

I put more frequent low effort updates on <lbry://@MyBeansAreBaking#3>

## License

Copyright (C) 2022 MyBeansAreBaked

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
