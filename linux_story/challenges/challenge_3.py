#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

from ..Step import Step
from challenge_4 import Step1 as Step1_next


class Step1(Step):
    story = [
        "Can we change the permissions of the note we just wrote?",
        "The command 'chmod' changes the permissions of files",
        "To make something writable, we use the command 'chmod +w filename'",
        "To remove the write permissions, use the command 'chmod -w filename'",
        "Run the command 'chmod -w note'"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = "chmod -w note",
    hint = "Type the command \"chmod -w note\" to stop the rabbit writing on your note"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step2()


class Step2(Step):
    story = [
        "If we use ls -l, we'll see that the note has lost it's "
        "write permissions",
        "Try using the command 'ls -l'"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = "ls -l"
    hint = "Type the command \"ls -l\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step3()


class Step3(Step):
    story = [
        "See, now our note has permissions -r--r--r--",
        "This means people can only read it, but can't write to it",
        "Let's have a look what's in the unlocked_door",
        "To see everything in a directory, use ls -a [directory_name]"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = "ls -a locked_door"
    hint = "Type the command \"ls -a locked_door\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step1_next()
