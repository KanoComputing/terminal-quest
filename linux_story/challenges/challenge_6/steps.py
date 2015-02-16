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
from linux_story.challenges.challenge_7.steps import Step1 as NextChallengeStep


class StepTemplateCd(Step):
    challenge_number = 6

    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gb:Congratulations, you earned 10 XP!}}\n",
        "Let mum know about Dad. Type {{yb:cat mum}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "cat mum"
    hints = "{{r:To talk to your mum, type}} {{yb:cat mum}} {{r:and press Enter}}."

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Mum: \"You couldn't find him either? Oh dear - this isn't good. "
        "He never leaves home without telling me first.\"",
        "\"Maybe he went to the town meeting with the Mayor. "
        "Why don't you go and check? I'll stay here in case he comes "
        "back.\"\n",
        "Let's go to town. To leave the house, use {{yb:cd}} by itself"
    ]
    start_dir = "kitchen"
    end_dir = "~"
    command = ""
    hints = "{{r:Type}} {{yb:cd}} {{r:to start the journey.}}"

    def block_command(self, line):
        allowed_commands = ["cd"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "You have left your house and are on a long road.",
        "Look around again to see where to go next."
    ]
    start_dir = "~"
    end_dir = "~"
    command = "ls"
    hints = "{{r:Stuck?  Type}} {{yb:ls}} {{r:to look around.}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "There's the town in the distance! Let's walk into town using "
        "{{yb:cd}}."
    ]
    start_dir = "~"
    end_dir = "town"
    command = ""
    hints = "{{r:Type}} {{yb:cd town}} {{r:to walk into town.}}"

    last_step = True

    def block_command(self, line):
        allowed_commands = ["cd town", "cd town/"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        NextChallengeStep()
