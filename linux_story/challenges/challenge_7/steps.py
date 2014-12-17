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
from linux_story.challenges.challenge_8.steps import Step1 as NextChallengeStep
from linux_story.file_functions import write_to_file
from linux_story.file_data import copy_data


class StepTemplateCd(Step):
    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gCongratulations, you earned 30 XP!}}\n",
        "Have a look around to see what's going on in town"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "To look around, use {{yls}}"

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Wow, there's so many people here. Find the mayor and see what's going on!"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "cat mayor"
    hints = "Stuck? Type: {{ycat mayor}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Mayor: \"Calm down please! We have our best people looking into the "
        "disappearances, and we're hoping to have an explanation soon\"\n",
        "Something strange is happening. Better check everyone is ok.",
        "Type {{ycat}} to check on everyone"
    ]
    start_dir = "town"
    end_dir = "town"

    # Use functions here
    command = ""
    all_commands = ["cat grumpy-man", "cat old-woman", "cat young-girl", "cat little-boy"]

    def check_command(self, line, current_dir):
        # check through list of commands
        command_validated = False
        end_dir_validated = False
        self.hints = ["Use {{y" + self.all_commands[0] + "}} to progress"]

        # strip any spaces off the beginning and end
        line = line.strip()

        end_dir_validated = current_dir == self.end_dir

        # if the validation is included
        if line in self.all_commands and end_dir_validated:
            self.all_commands.remove(line)

            if len(self.all_commands) > 0:
                # This needs to be green
                self.save_hint("\nWell done!  Check on {} more people".format(len(self.all_commands)))
            else:
                command_validated = True

        else:
            self.save_hint("\n" + self.hints[0])

        return command_validated and end_dir_validated

    def next(self):
        write_to_file("challenge", "8")
        copy_data(8)
        NextChallengeStep()
