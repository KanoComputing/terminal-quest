
# Terminal Quest

This is the source code for the Terminal Quest app available for Kano OS.
It is an introduction to terminal commands in the style of a text adventure game.

# How to install it

## Kano OS
linux-story is installed by default on Kano OS, and is provided as a debian package in our repositories. As it has a lot of dependencies from other packages in Kano OS, it is recommended you run it on Kano OS.
 - Package name: linux-story
 - Executable: /usr/bin/linux-story-gui

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
