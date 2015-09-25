
# Terminal Quest

This is the source code for the Terminal Quest app available for Kano OS.
It is an introduction to terminal commands in the style of a text adventure game.

# Translation in Italian going on

## by Andreas Formiconi

The first 10 challenges have been translated, so far.

In the challenge\_\*.py files the English textis have been left,
commented with \#arf, in the meanwhile

The italian versions of the objects have been put in folder
linux\_story/ascii\_assets/story\_files/it/

In this version an interruption was provided in 
bin/linux\_story (instructions 35-38)

in case the program is launched via command line with a challenge
number greater then 10

and in
linux\_story/story/challenges/challenge\_10.py (instructions 275-277)

in case one comes from challenge 10.

This Italian version is localized for kids living in Tuscany. 


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
