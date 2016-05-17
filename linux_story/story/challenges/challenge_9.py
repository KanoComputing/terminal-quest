# challenge_9.py
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
from linux_story.story.challenges.challenge_10 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(TerminalCd):
    challenge_number = 9


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        _("Oh no! Check your {{bb:Mum}} is alright.\n"),
        _("Type {{yb:cd ..}} to leave {{bb:town}}.")
    ]
    start_dir = "~/town"
    end_dir = "~"
    commands = ["cd ..", "cd ../", "cd"]
    hints = _("{{rb:Use}} {{yb:cd ..}} {{rb:to start heading back home.}}")

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        _("{{pb:Ding. Dong.}}\n"),
        _("Type {{yb:cd my-house/kitchen}} to go straight to the "
          "{{bb:kitchen}}.\n"),
        _("{{gb:Press}} {{ob:TAB}} {{gb:to speed up your typing!}}")
    ]
    start_dir = "~"
    end_dir = "~/my-house/kitchen"
    commands = ["cd my-house/kitchen", "cd my-house/kitchen/"]
    hints = [
        _("{{rb:Use}} {{yb:cd my-house/kitchen}} {{rb:to go to the "
          "kitchen.}}")
    ]
    story_dict = {
        "note_kitchen": {
            "name": "note",
            "path": "~/my-house/kitchen"
        }
    }
    # Remove the note as well.
    deleted_items = ['~/my-house/kitchen/Mum', '~/town/note']

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        _("Take a {{lb:look around}} to make sure everything is OK.")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = "ls"
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to see that everything is where it "
          "should be.}}")
    ]

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        _("Oh no - {{bb:Mum}} has vanished too!"),
        _("Wait, there's another {{bb:note}}.\n"),
        _("Use {{yb:cat}} to {{lb:read}} the {{bb:note}}.")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = "cat note"
    hints = _("{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}")
    last_step = True

    def next(self):
        NextStep(self.xp)
