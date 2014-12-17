#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

import os
import sys
import time

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
        "Have a look around to see what's going on in town."
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "{{rTo look around, use}} {{yls}}"

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Wow, there's so many people here. Find the mayor and see what's going on!"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "cat mayor"
    hints = "{{rStuck? Type:}} {{ycat mayor}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Mayor: \"Calm down please! We have our best people looking into the "
        "disappearances, and we're hoping to have an explanation soon.\"\n",
        "Something strange is happening. Better check everyone is ok.",
        "Type {{ycat}} to check on everyone."
    ]
    start_dir = "town"
    end_dir = "town"

    # Use functions here
    command = ""
    all_commands = {
        "cat grumpy-man": "Man: \"I don't know what's happening to me"
        " - my legs have gone all bendy!\"",
        "cat young-girl": "Girl: \"I can't find my friend Amy anywhere. If you see her, "
        "will you let me know?\"",
        "cat little-boy": "Boy: \"Has anyone seen my dog Bernard? He's never run away before...\""
    }

    def check_command(self, line, current_dir):
        # check through list of commands
        command_validated = False
        end_dir_validated = False
        self.hints = ["{{rUse}} {{y" + self.all_commands.keys()[0] + "}} {{rto progress}}"]

        # strip any spaces off the beginning and end
        line = line.strip()

        end_dir_validated = current_dir == self.end_dir

        # if the validation is included
        if line in self.all_commands.keys() and end_dir_validated:
            # Print hint from person
            hint = "\n" + self.all_commands[line]

            self.all_commands.pop(line, None)

            if self.all_commands == 1:
                hint += "\n{{gWell done! Check on 1 more person.}}"
            elif len(self.all_commands) > 0:
                hint += "\n{{gWell done! Check on " + \
                    str(len(self.all_commands)) + \
                    " more people.}}"
            else:
                command_validated = True

            self.save_hint(hint)

        else:
            self.save_hint("\n" + self.hints[0])

        return command_validated and end_dir_validated

    def next(self):
        time.sleep(6)
        write_to_file("challenge", "8")
        copy_data(8)
        NextChallengeStep()
