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
from linux_story.challenges.challenge_6.steps import Step1 as NextChallengeStep
from linux_story.file_functions import write_to_file
from linux_story.file_data import copy_data


class StepTemplateCd(Step):
    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gCongratulations, you earned 20 XP!}}\n",
        "Mum: \"Have you seen your Dad? I can't find him anywhere, "
        "and the newspaper says that people have been going missing all over Folderton!\"\n",
        "Let's look for your Dad in the garden",
        "To go to the garden, type {{ycd garden}}"
    ]
    start_dir = "kitchen"
    end_dir = "garden"
    command = ""
    hints = "{{rTo go to the garden, type}} {{ycd garden}}"

    def block_command(self, line):
        allowed_commands = ["cd garden", "cd garden/"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            self.save_hint("Careful! You want to go to the {{bgarden}}")
            return True

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Use {{yls}} to look in the garden for your Dad"
    ]
    start_dir = "garden"
    end_dir = "garden"
    command = "ls"
    hints = "{{rTo look for your Dad, type}} {{yls}} {{rand press Enter}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Hmmm...you can't see him anywhere",
        "Maybe he's in the {{ygreenhouse}}.  Go into the greenhouse."
    ]
    start_dir = "garden"
    end_dir = "greenhouse"
    command = ""
    hints = "{{rTo go to the greenhouse, type}} {{ycd greenhouse}}"

    def block_command(self, line):
        allowed_commands = ["cd greenhouse", "cd greenhouse/"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            self.save_hint("Careful! You want to go to the {{bgreenhouse}}")
            return True

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Is he here? Type {{yls}} to find out."
    ]
    start_dir = "greenhouse"
    end_dir = "greenhouse"
    command = "ls"
    hints = "{{rType}} {{yls}} {{rto look for your Dad.}}"

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "Hmmmm. He's not here. But there is something odd.",
        "You see a note on the ground.  Use {{ycat note}} to read what it says"
    ]
    start_dir = "greenhouse"
    end_dir = "greenhouse"
    command = "cat note"
    hints = "{{rType}} {{ycat note}} {{rto see what the note says!}}"

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "Going back is super easy. Just type {{ycd ..}} to go back the way you came."
    ]
    start_dir = "greenhouse"
    end_dir = "garden"
    command = ""
    hints = "{{rType}} {{ycd ..}} {{rto go back to the garden}}"

    def block_command(self, line):
        allowed_commands = ["cd ..", "cd ../"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            self.save_hint("{{rCareful! You want to go back using}} {{ycd ..}}")
            return True

    def next(self):
        Step7()


class Step7(StepTemplateCd):
    story = [
        "You're back in the garden.  Use {{ycd ..}} again to go back to the kitchen."
    ]
    start_dir = "garden"
    end_dir = "kitchen"
    command = ""
    hints = "{{rType}} {{ycd ..}} {{rto go back to the kitchen}}"

    last_step = True
    challenge_number = 5

    def block_command(self, line):
        allowed_commands = ["cd ..", "cd ../"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            self.save_hint("Careful! You want to go back using {{ycd ..}}")
            return True

    def next(self):
        write_to_file("challenge", "6")
        copy_data("6")
        NextChallengeStep()
