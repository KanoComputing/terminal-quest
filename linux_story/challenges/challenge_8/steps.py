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
from linux_story.file_functions import write_to_file


class StepTemplateCd(Step):
    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gCongratulations, you earned 35 XP!}}\n",
        "What was that?  A rumble?",
        "Use {{yls}} to see what happened."
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "{{rTo look around, use}} {{yls}}"

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Everyone has gone.",
        "Wait - there's just a note on the floor.",
        "Use {{ycat}} to read the note"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "cat note"
    hints = "{{rTo look around, use}} {{ycat note}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Type {{ycd ..}} until you get back to the {{bkitchen}}"
    ]
    start_dir = "town"
    end_dir = "kitchen"
    command = ""
    hints = "{{rUse}} {{ycd ..}} {{rto progress}}"
    allowed_commands = ["cd ..", "cd ../"]

    def __init__(self):
        self.counter = 0
        StepTemplateCd.__init__(self)

    def block_command(self, line):
        line = line.strip()
        if "cd" in line and line not in self.allowed_commands:
            return True

    def check_command(self, line, current_dir):
        # check through list of commands
        command_validated = False

        # strip any spaces off the beginning and end
        line = line.strip()

        # if the validation is included
        if line in self.allowed_commands:
            self.counter += 1

            if self.counter > 2:
                command_validated = True

            else:
                # Print hint from person
                hint = "\n{{gWell done!  Keep going!}}"
                self.save_hint(hint)

        else:
            self.save_hint("\n" + self.hints[0])

        return command_validated

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Check if everything is where it should be.  Look around."
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "ls"
    hints = "{{rUse}} {{yls}} {{rto see that everything is where it should be}}"

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "Oh no - Mum's vanished too.",
        "Wait - there's another note.",
        "Use {{ycat}} to read the note"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "cat note"
    hints = "{{rUse}} {{ycat note}} {{rto read the note}}"

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "{{rTo be continued...}}\n",
        "Press any key to exit"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = ""

    def next(self):
        write_to_file("exit")
