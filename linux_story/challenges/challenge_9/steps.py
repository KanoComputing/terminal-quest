#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.Step import Step
from linux_story.challenges.challenge_4.terminals import TerminalCd
from linux_story.challenges.challenge_10.steps import Step1 as NextStep
from linux_story.helper_functions import play_sound
from linux_story.file_data import copy_data


class StepTemplateCd(Step):
    challenge_number = 9

    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gb:Congratulations, you earned 25 XP!}}\n",
        "Oh no! Check your Mum is alright.",
        "Type {{yb:cd ..}} to leave town."
    ]
    start_dir = "town"
    end_dir = "~"
    command = ""
    hints = "{{r:Use}} {{yb:cd ..}} {{r:to progress.}}"

    def block_command(self, line):
        allowed_commands = ["cd ..", "cd ../"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        play_sound('bell')
        copy_data(9, 2)
        Step2()


class Step2(StepTemplateCd):
    story = [
        "{{pb:Ding. Dong.}}",
        "Type {{yb:cd my-house/kitchen}} to go straight to the kitchen"
    ]
    start_dir = "~"
    end_dir = "kitchen"
    command = ""
    hints = "{{r:Use}} {{yb:cd my-house/kitchen}} {{r:to go to the kitchen.}}"

    def block_command(self, line):
        allowed_commands = ["cd my-house/kitchen", "cd my-house/kitchen/"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Check if everything is where it should be. Look around."
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "ls"
    hints = [
        "{{r:Use}} {{yb:ls}} {{rn:to see that everything is where it "
        "should be.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Oh no - Mum's vanished too.",
        "Wait - there's another note.",
        "Use {{yb:cat}} to read the note."
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "cat note"
    hints = "{{r:Use}} {{yb:cat note}} {{rn:to read the note.}}"
    last_step = True

    def next(self):
        copy_data(10, 1)
        NextStep()
