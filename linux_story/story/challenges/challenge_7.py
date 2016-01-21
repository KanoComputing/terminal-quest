# challenge_7.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_8 import Step1 as NextChallengeStep


class StepTemplateCd(TerminalCd):
    challenge_number = 7


class Step1(StepTemplateCd):
    story = [
        "Have a {{lb:look around}} to see what's going on!"
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = "{{rb:To look around, use}} {{yb:ls}}"

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Wow, there's so many people here. Find the {{lb:Mayor}} and "
        "{{lb:listen}} to what he has to say."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "cat Mayor"
    hints = "{{rb:Stuck? Type:}} {{yb:cat Mayor}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "{{wb:Mayor:}} {{Bb:\"Calm down please! We have our best "
        "people looking into the disappearances, and we're hoping to "
        "have an explanation soon.\"}}\n",
        "Something strange is happening. Better check everyone is ok.",
        "Type {{lb:cat}} to check on the people."
    ]
    start_dir = "~/town"
    end_dir = "~/town"

    # Use functions here
    command = ""
    all_commands = {
        "cat grumpy-man": "\n{{wb:Man:}} {{Bb:\"Help! I don't know what's "
        "happening to me. I heard this bell ring, and now my legs have "
        "gone all strange.\"}}",
        "cat young-girl": "\n{{wb:Girl:}} {{Bb:\"Can you help me? I can't "
        "find my friend Amy anywhere. If you see her, will you let me"
        " know?\"}}",
        "cat little-boy": "\n{{wb:Boy:}} {{Bb:\"Pongo? Pongo? Has "
        "anyone seen my dog Pongo? He's never run away before...\"}}"
    }

    last_step = True

    def check_command(self):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if self.last_user_input == 'ls':
            hint = "\n{{gb:Well done for looking around.}}"
            self.send_text(hint)
            return False

        # check through list of commands
        end_dir_validated = False
        self.hints = [
            "{{rb:Use}} {{yb:" + self.all_commands.keys()[0] + "}} "
            "{{rb:to progress.}}"
        ]

        end_dir_validated = self.current_path == self.end_dir

        # if the validation is included
        if (self.last_user_input in self.all_commands.keys()) and \
                end_dir_validated:
            # Print hint from person
            hint = "\n" + self.all_commands[self.last_user_input]

            self.all_commands.pop(self.last_user_input, None)

            if len(self.all_commands) == 1:
                hint += "\n{{gb:Well done! Check on 1 more person.}}\n"
            elif len(self.all_commands) > 0:
                hint += "\n{{gb:Well done! Check on " + \
                    str(len(self.all_commands)) + \
                    " more people.}}\n"
            else:
                hint += "\n{{gb:Press {{ob:Enter}} to continue.}}"

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        NextChallengeStep(self.xp)
