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
from terminals import TerminalCd
from linux_story.challenges.challenge_5.steps import Step1 as NextChallengeStep
#from linux_story.file_data import copy_data
from linux_story.file_functions import write_to_file


class StepTemplateCd(Step):
    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gCongratulations, you earned 15 XP!}}\n",
        "That's weird. No time for that now though - lets find Mum.",
        "\n{{wNew Spell}}: {{ycd}} lets you move between places.",
        "\nType {{ycd kitchen}} to go and see Mum."
    ]
    start_dir = "~"
    end_dir = "kitchen"
    command = ""
    hints = "{{rType}} {{ycd kitchen}} {{rto go to the kitchen}}"

    def block_command(self, line):
        allowed_commands = ["cd kitchen", "cd kitchen/"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            self.save_hint("Careful! You want to go to the {{ykitchen}}.")
            return True

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "You are in the kitchen.",
        "Try and find Mum using {{yls}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "ls"
    hints = "{{rCan't find her?  Type}} {{yls}} {{rand press Enter.}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Let's see what {{ymum}} wants by using {{ycat}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "cat mum"
    hints = "{{rStuck? Type:}} {{ycat mum}}"

    def next(self):
        #copy_data(5)
        write_to_file("challenge", "5")
        NextChallengeStep()
