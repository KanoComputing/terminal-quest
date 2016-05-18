# challenge_13.py
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

from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_14 import Step1 as NextStep
from linux_story.step_helper_functions import (
    unblock_commands_with_cd_hint, unblock_commands
)


class StepTemplateMv(TerminalMv):
    challenge_number = 13


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        _("{{wb:Edward:}} {{Bb:\"Thank you so much for saving my little girl!"),
        _("I have another favour to ask..."),
        _("We haven't got any food. Could you gather some for us? We didn't have time to grab any before we went into hiding.\""),
        _("\"Do you remember seeing any food in your travels?\"}}"),
        _("\n...ah! You have all that food in your {{bb:kitchen}}! We could give that to this family."),
        _("\nStart by {{lb:moving}} the {{bb:basket}} to {{bb:~}}. Use the command {{yb:mv basket ~/}}\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "mv basket ~",
        "mv basket/ ~",
        "mv basket ~/",
        "mv basket/ ~/",
        "mv basket ../..",
        "mv basket/ ../..",
        "mv basket ../../",
        "mv basket/ ../../"
    ]
    hints = [
        _("{{rb:Use the command}} {{yb:mv basket ~/}} {{rb:to move the}} {{bb:basket}} {{rb:to the windy road}} {{bb:~}}")
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        _("Now follow the {{bb:basket}}. Use {{yb:cd}} by itself to {{lb:go}} to the windy road Tilde {{bb:~}}.\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~"
    commands = [
        "cd",
        "cd ~",
        "cd ~/"
    ]
    hints = [
        _("{{rb:Use the command}} {{yb:cd}} {{rb:by itself to move yourself to the road ~}}")
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        _("You are now back on the long windy road. {{lb:Look around}} with {{yb:ls}} to check that you have your {{bb:basket}} with you.\n")
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
        "ls"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:by itself to look around.}}")
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        _("You have your {{bb:basket}} safely alongside you, and you see {{bb:my-house}} close by."),
        _("Move the {{bb:basket}} to {{bb:my-house/kitchen}}."),
        _("Don't forget to use the {{ob:TAB}} key to autocomplete your commands.\n")
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
        "mv basket my-house/kitchen",
        "mv basket/ my-house/kitchen",
        "mv basket my-house/kitchen/",
        "mv basket/ my-house/kitchen/",
        "mv basket ~/my-house/kitchen",
        "mv basket/ ~/my-house/kitchen",
        "mv basket ~/my-house/kitchen/",
        "mv basket/ ~/my-house/kitchen/"
    ]
    hints = [
        _("{{rb:Use}} {{yb:mv basket my-house/kitchen/}} {{rb:to move the basket to your kitchen.}}"),
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        _("Now {{lb:go}} into {{bb:my-house/kitchen}} using {{yb:cd}}.\n"),
    ]

    start_dir = "~"
    end_dir = "~/my-house/kitchen"
    commands = [
        "cd my-house/kitchen",
        "cd my-house/kitchen/",
        "cd ~/my-house/kitchen",
        "cd ~/my-house/kitchen/"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cd my-house/kitchen}} {{rb:to go to your kitchen.}}"),
    ]
    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextStep(self.xp)
