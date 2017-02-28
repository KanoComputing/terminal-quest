
# Terminal Quest

This is the source code for the Terminal Quest app available for Kano OS.
It is an introduction to terminal commands in the style of a text adventure game.

# How to install it

## Kano OS
linux-story is installed by default on Kano OS, and is provided as a debian package in our repositories. As it has a lot of dependencies from other packages in Kano OS, it is recommended you run it on Kano OS.
 - Package name: linux-story
 - Executable: /usr/bin/linux-story-gui

### A word about nano

Terminal Quest currently comes with a custom build of the `nano` editor that integrates the adventure GUI workflow.
It is packaged in binary form on this repo. If you need to recompile it for whatever reason:

```
$ sudo apt-get install build-essential automake autoconf libncurses-dev texinfo -y --no-install-recommends
$ cd nano-2.2.6

$ ./configure --disable-browser --disable-extra --disable-mouse --disable-glibtest (???)

$ ./configure --disable-browser --disable-extra --disable-mouse --disable-glibtest
$ make localedir=/usr/share/locale sysconfdir=/etc
$ strip src/nano
$ git add nano ; git commit ; git push
```

At the moment, `nano` will automatically pick up the translated messages from the official nano installed on Kano OS,
hence picking up translation files from `/usr/share/locale`.

FIXME: nano recompilation is not good - It decides to peek at `/usr/lib/locale/es_AR/LC_IDENTIFICATION` and gives up.

# How Terminal Quest works
For a more detailed breakdown, read the [development wiki page](https://github.com/KanoComputing/linux-tutorial/wiki/Development).

# Options

```
linux-story-gui launches the application Terminal Quest at different points in the story.

Usage:
  linux-story-gui [-d | --debug]
  linux-story-gui challenge <challenge> <step> [-d | --debug]

Options:
   -h, --help       Show this message.
   -d, --debug      Debug mode, don't hide the terminal and spellbook widgets by default at the start.
```

Make sure your environment exposes `PYTHONIOENCODING=UTF-8` for correct i18n translations throughout the adventure.
