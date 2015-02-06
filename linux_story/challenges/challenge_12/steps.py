#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.Step import Step
from linux_story.challenges.challenge_11.terminals import TerminalMv


class StepTemplateMv(Step):
    challenge_number = 11

    def __init__(self):
        Step.__init__(self, TerminalMv)


# When you talk to Graham
class Step1(StepTemplateMv):
    story = [
        "Graham:  Hey, since you don't seem to be affected by going outside, "
        "can you gather some food for us? ",
        "We didn't have time to grab any before we went into hiding.\n",
        "Have a look outside for additonal food. Start by leaving the "
        ".hidyhole."
    ]
    start_dir = ".hidyhole"
    end_dir = "town"
    command = ""
    hints = [
        "{{r:Use the command}} {{y:cd ..}}"
    ]

    def next(self):
        Step2()


# In town, look for possible places
class Step2(StepTemplateMv):
    story = [
        "You are back in town.",
        "There are a lot of houses that seem to be deserted."
    ]
    start_dir = "town"
    end_dir = "town"
    command = ""
    hints = [
        "{{r:Use the command}} {{y:ls -a}} {{r:to see the hidden folders}}"
    ]

    def next(self):
        pass

# Find a directory that looks like it co
