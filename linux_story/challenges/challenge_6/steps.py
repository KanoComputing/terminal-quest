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
from linux_story.file_functions import write_to_file


class StepTemplateCd(Step):
    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gCongratulations, you earned 25 XP!}}\n",
        "Let mum know about Dad. Type {{ycat mum}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "cat mum"
    hints = "{{rTo talk to your mum, type}} {{ycat mum}} {{rand press Enter}}."

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Mum: \"You couldn't find him either? Oh dear - this isn't good. "
        "He never leaves home without telling me first.\"",
        "\"Maybe he went to the town meeting with the Mayor. "
        "Why don't you go and check? I'll stay here in case he comes back.\"\n",
        "Let's go to town. Type {{ycd garden}} to start the journey."
    ]
    start_dir = "kitchen"
    end_dir = "garden"
    command = ""
    hints = "{{rType}} {{ycd garden}} {{rto start the journey.}}"

    def block_command(self, line):
        allowed_commands = ["cd garden", "cd garden/"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Look around again to see where to go next."
    ]
    start_dir = "garden"
    end_dir = "garden"
    command = ""
    hints = "{{rStuck?  Type}} {{yls}} {{rto look around.}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "There's a road! Let's have a look down the road.",
        "Type {{yls road}} to look down the road."
    ]
    start_dir = "garden"
    end_dir = "garden"
    command = ["ls road", "ls road/"]
    hints = "{{rType}} {{yls road}} {{rto look down the road.}}"

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "There's the town! Let's walk into town using {{ycd}}"
    ]
    start_dir = "garden"
    end_dir = "town"
    command = ""
    hints = "{{rType}} {{ycd road/town}} {{rto walk into town.}}"

    def block_command(self, line):
        allowed_commands = ["cd road/town", "cd road/town/"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        write_to_file("challenge", "7")
        NextChallengeStep()
