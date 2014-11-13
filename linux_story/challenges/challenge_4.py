#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

from ..Step import Step


class Step1(Step):
    story = [
        "So what does this key do?",
        "I reckon it's got something to do with the locked_door directory",
        "Let's read the .key file"
    ]
    start_dir = "rabbithole",
    end_dir = "rabbithole",
    command = "less .key",
    hint = "Type the command \"less .key\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step2()


class Step2(Step):
    story = [
        "So the key contains some linux commands",
        "We learnt the chmod one earlier - this one changes the permissions of files",
        "The line 'chmod +rw locked_door' stops the directory being readbale or writable",
        "What does the 'mv' command do?  Let's look it up!",
        "Use the command 'man mv' to look up the mv command"
    ]
    start_dir = "rabbithole",
    end_dir = "rabbithole",
    command = "man mv",
    hint = "Type the command \"man mv\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step3()


class Step3(Step):
    story = [
        "So 'mv' MoVes or renames files",
        "Let's try it out.  Try moving the .key into the .trapdoor directory",
        "Use the command 'mv .key .trapdoor/"
    ]
    start_dir = "rabbithole",
    end_dir = "rabbithole",
    command = "mv .key .trapdoor/",
    hint = "Type the command \"mv .key .trapdoor/\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step4()


class Step4(Step):
    story = [
        "Well done!  Run the ls command to check the key has indeed moved",
        "Check this directory first",
        "Run ls -a"
    ]
    start_dir = "rabbithole",
    end_dir = "rabbithole",
    command = "ls -a",
    hint = "Type the command \"ls -a\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step5()


class Step5(Step):
    story = [
        "See, the .key file has moved from this directory",
        "Check it moved to the .trapdoor directory"
    ]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "ls -a .trapdoor/"
    hint = "Type the command \"ls -a .trapdoor/\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step6()


class Step6(Step):
    story = [
        "So we correctly moved the key from this directory to the .trapdoor directory",
        "Now lets inspect this .key a little more.",
        "Wouldn't it be cool to be able run the commands in this file"
        " without copying them into a terminal?",
        "We can run the command, but only if the file is executable.",
        "To make a file executable, use the command chmod",
        "Run the command 'chmod +x .trapdoor/.key'"
    ]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "chmod +x .trapdoor/.key"
    hint = "Type the command \"chmod +x .trapdoor/.key\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step7()


class Step7(Step):
    story = [
        "Now use 'ls -la .trapdoor' to have a closer look at the key",
        "Notice you can combine flags.  'ls -l -a .trapdoor'"
        "will do the same thing"
    ]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = ["ls -la .trapdoor", "ls -la .trapdoor/"]
    hint = "Type the command \"ls -la .trapdoor\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step8()


class Step8(Step):
    story = [
        "Notice now the permissions of the key has gone "
        "from -rw-rw-r-- to -rwxrwxr-x ",
        "The x at the end means it has become executable.",
        "Notice also the file name has changed colour",
        "Let's try and run it!  To run a shell script, type out it's file path",
        "Run the command '.trapdoor/.key'"
    ]
    start_dir = "rabbithole",
    end_dir = "rabbithole",
    command = ".trapdoor/.key",
    hint = "Type the command \".trapdoor/.key\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step9()


class Step9(Step):
    story = ["Use ls to see what it's done"]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "ls .trapdoor"
    hint = "Type the command \"ls .trapdoor\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step10()


class Step10(Step):
    story = [
        "So the directory has been renamed to 'unlocked_door'",
        "This makes sense.  Remember the 'mv' command also renames files",
        "Remember it also removed the readbale and writable permissions "
        "to the directory",
        "What does this mean?  Try using cd to get into the directory"
    ]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "cd .trapdoor/locked_door"
    hint = "Type the command \"cd .trapdoor/locked_door\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step11()


class Step11(Step):
    story = [
        "We can get in to the directory!",
        "So this is why it's now unlocked",
        "How do we lock it?",
        "Modify the .key file so that it locks the unlocked_door"
    ]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "nano .trapdoor/.key"
    hint = "Type the command \"nano .trapdoor/.key to modify the .key file\""

    def __init__(self):
        Step.__init__(self)
