VLC Sync
========

Utility for synchronize multiple instances of VLC. Supports seek, play and pause. 
Inspired by F1 streams with extra driver tracking data.  

# Run

`Vlc` instances should expose "Remote control interface" on 127.0.0.42 (see [how configure vlc](./docs/vlc_setup.md))

```shell

# Run vlc (should with open --rc-host 127.0.0.42 option) 
$ vlc --rc-host 127.0.0.42 SomeMedia1.mkv &
$ vlc --rc-host 127.0.0.42 SomeMedia2.mkv &
$ vlc --rc-host 127.0.0.42 SomeMedia3.mkv &

# vlcsync will find all vlc on 127.0.0.42:* and start syncing 
$ vlcsync

Vlcsync started...
Found instance with pid 3538289 and port 127.0.0.42:34759 State(play_state=playing, seek=10)
Found instance with pid 3538290 and port 127.0.0.42:38893 State(play_state=playing, seek=10)
Found instance with pid 3538291 and port 127.0.0.42:45615 State(play_state=playing, seek=10)
```

## Install

```shell
pip3 install -U vlcsync
```

## Status 

In development. Tested on Linux, but should also work on Win/macOS.

Any thoughts, ideas and contributions welcome!

Roadmap:

- [ ] Add ability to set static addresses i.e. for remote sync (to external pc/screen)
- [ ] Add portable `*.exe` build for Windows

## Demo

![](./docs/vlcsync.gif)

Enjoy! 🚀