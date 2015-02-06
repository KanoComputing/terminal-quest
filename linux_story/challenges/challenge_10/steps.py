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
from linux_story.challenges.challenge_4.terminals import TerminalCd
from linux_story.challenges.challenge_11.steps import Step1 as NextStep


class StepTemplateCd(Step):
    challenge_number = 9

    def __init__(self):
        Step.__init__(self, TerminalCd)


############################################################################
# This is the difficult bit to get through
# In this level, try ad find lots of corrupted ascii art around the kicthen?
# So encourage them to use cat in a few places

class Step1(StepTemplateCd):
    story = [
        "{{gb:Congratulations, you earned 25 XP!}}\n",
        "You're in your house.  You appear to be alone.",
        "Use {{yb:cat}} to have a look at some of the objects around you."
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = ""
    hints = "{{r:Look at some of the objects using}} {{y:cat}}"

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "There appears to be nothing here.  See if you can find something "
        "outside the house"
    ]
    start_dir = "kitchen"
    end_dir = "town"
    command = ""
    hints = [
        "{{r:See if there is anything back in the town}}",
        "{{r:Use}} {{yb:cd}} {{r:to get back into town}}"
    ]

    def block_command(self, line):
        allowed_commands = [
            "cd ~/town",
            "cd ~/town/",
            "cd ..",
            "cd ../",
            "cd town",
            "cd town/",
            "cd"
        ]

        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        Step3()
############################################################################


class Step3(StepTemplateCd):
    story = [
        "Have a look around",
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "{{r:Use}} {{yb:ls}} {{r:to have a look around the town}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "You can't see much here.  The place appears to be deserted.",
        "However, you think you hear whispers.",
        # Make this writing small
        "{{wn:\".....if they use}} {{yb:ls -a}}{{wn:, they'll see us...\"}}",
        "{{wn:\"..Shhh!  ...might hear....\"}}"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls -a"
    hints = [
        "{{r:You heard whispers referring to}} {{yb:ls -a}}"
        "{{r:, try using it!}}",
    ]

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "You see a {{yb:.hidyhole}} that you didn't notice before.",
        "It sounds like there is where the whispers are coming from."
    ]
    start_dir = "town"
    end_dir = ".hidyhole"
    command = ""
    hints = [
        "{{r:Try going inside the}} {{yb:.hidyhole}} {{r:using}} {{yb:cd}}",
        "{{r:Use the command {{yb:cd .hidyhole}} to see where the whispers "
        "are coming from}}"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "Have a look around."
    ]
    start_dir = ".hidyhole"
    end_dir = ".hidyhole"
    command = "ls"
    hints = [
        "{{r:Use}} {{yb:ls}} {{r:to have a look around you}}"
    ]

    def next(self):
        NextStep()
