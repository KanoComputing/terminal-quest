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
        "\nMaybe we should take a closer look at the key",
        "Read the contents of the key file",
        "Use the command 'less .key'"
    ]
    start_dir = "rabbithole"
    end_dir = ""
    hint = ""
    command = ""
    hint = "Type the command \"less .key\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step2()


class Step2(Step):
    story = [
        "\nSome of these commands look familiar",
        "We learnt before that chmod would change the permission on the key",
        "But I don't think this key is in the right directory",
        "Try moving the key to the directory above"
    ]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "mv .key .trapdoor"
    structure = ""
    hint = "Type the command \"mv .key .trapdoor\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step3()


class Step3(Step):
    story = [
        "\nOK!  Now we could run the commands in the .key file individually",
        "But wouldn't it be good if we could run the commands in the file directly?",
        "Lets check out the permissions of the file",
        "Do you remember how to find out more about a file?"
    ]
    start_dir = "rabbithole"
    end_dir = ".trapdoor"
    command = "ls -la"
    hint = "Type the command \"ls -la\" in the .trapdoor directory"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step4()


class Step4(Step):
    story = [
        "\nIf we make this file executable, we can run the commands in the file",
        "We can see this file is readable only",
        "Lets change it so it's also executable"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = "chmod +x .key"
    hint = "Type the command \"chmod +x .key\" in the .trapdoor directory"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step5()


class Step5(Step):
    story = [
        "\nExcellent!  Now let's run the script",
        "Use .key to run the executible file"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = ".key"
    hint = "Type the command \".key\" in the .trapdoor directory"
    animation = "rabbit.py 1 right-to-left"

    def __init__(self):
        Step.__init__(self)
