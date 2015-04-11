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
from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_8 import Step1 as NextChallengeStep
from linux_story.helper_functions import play_sound


class StepTemplateCd(Step):
    challenge_number = 7

    def __init__(self, xp=""):
        Step.__init__(self, TerminalCd, xp)


class Step1(StepTemplateCd):
    story = [
        "Have a look around to see what's going on!"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "{{rb:To look around, use}} {{yb:ls}}"

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "It looks like the whole town has come to the meeting. Find the {{yb:Mayor}} and see "
        "what's going on!"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "cat Mayor"
    hints = "{{rb:Stuck? Type:}} {{yb:cat Mayor}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "{{wb:Mayor:}} {{Bn:\"People of Folderton please Calm down! We have the scientists "
        "at Folderton University looking into the disappearances. We're hoping to "
        "have an explanation soon and then all this can be sorted out.\"}}\n",
        "Not even the Mayor knows what's going on! Better check everyone is ok.",
        "Type {{yb:cat}} to check on the people."
    ]
    start_dir = "town"
    end_dir = "town"

    # Use functions here
    command = ""
    all_commands = {
        "cat grumpy-man": "\n{{wb:Man:}} {{Bn:\"Help! I don't know what's "
        "happening to me. I heard this bell ring, and now my legs have "
        "gone all strange.\"}}",
        "cat young-girl": "\n{{wb:Girl:}} {{Bn:\"Can you help me? I can't find my "
        "friend Amy anywhere. Please! If you see her, will you let me know?\"}}",
        "cat little-boy": "\n{{wb:Boy:}} {{Bn:\"Bernard? Bernard? Has anyone seen my "
        "dog Bernard? He's never run away before...\"}}"
    }

    last_step = True

    def check_command(self, line, current_dir):

        if not self.all_commands:
            hint = "\n{{g:Press Enter to continue}}"
            return True

        # strip any spaces off the beginning and end
        line = line.strip()

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = "\n{{g:Nice work!}}"
            self.send_text(hint)
            return False

        # check through list of commands
        command_validated = False
        end_dir_validated = False
        self.hints = [
            "{{rb:Use}} {{yb:" + self.all_commands.keys()[0] + "}} "
            "{{rb:to progress}}"
        ]

        end_dir_validated = current_dir == self.end_dir

        # if the validation is included
        if line in self.all_commands.keys() and end_dir_validated:
            # Print hint from person
            hint = "\n" + self.all_commands[line]

            self.all_commands.pop(line, None)

            if len(self.all_commands) == 1:
                hint += "\n{{g:Well done! Check on 1 more person.}}"
            elif len(self.all_commands) > 0:
                hint += "\n{{g:Well done! Check on " + \
                    str(len(self.all_commands)) + \
                    " more people.}}"
            else:
                command_validated = True
                hint += "\n{{g:Press Enter to continue}}"

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        return command_validated and end_dir_validated

    def next(self):
        play_sound('bell')
        NextChallengeStep(self.xp)
