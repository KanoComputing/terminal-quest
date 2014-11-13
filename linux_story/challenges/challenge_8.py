#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

from ..Step import Step


class Step1(Step):
    story = ["Let's have a look around, see where you are"]
    start_dir = "woods"
    end_dir = "woods"
    command = "ls"
    hint = "Type the command \"ls\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step2()


class Step2(Step):
    story = [
        "Woah, that is a lot of trees",
        "I can't see where the rabbit could have got to.",
        "We need to look for a directory amoungst all these trees",
        "The command ls -d [extra info] will give you information about the directory "
        "specified by [all info]",
        "So ls -d *.txt will only show you the files that end in .txt",
        "We want to find information about the directories in this woods directory",
        "Try ls -d */"
    ]
    start_dir = "woods"
    end_dir = "woods"
    command = "ls -d */"
    hint = "Type the command \"ls -d *\/\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step3()


class Step3(Step):
    story = [
        "Cool, we found some possible places!",
        "You've come a long way and learnt a lot of commands",
        "If you need to look these commands up again, use 'man', short of MANual.",
        "Use the command 'man ls' to look up information about the ls command"
    ]
    start_dir = "woods"
    end_dir = "woods"
    command = "man ls"
    hint = "Type the command \"man ls\""

    def __init__(self):
        Step.__init__(self)
