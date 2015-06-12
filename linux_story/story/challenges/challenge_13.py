#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
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


class Step1(StepTemplateMv):
    story = [
        "{{wb:Edward:}} {{Bb:\"Thank you so much for saving my little girl!",
        "I have another favour to ask...",
        "We haven't got any food, could you gather some for us? "
        "We didn't have "
        "time to grab any before we went into hiding.\"",
        "\"Do you remember seeing any food in your travels?\"}}",
        "\n...ah! You have all that food in your {{lb:kitchen}}! "
        "We could give that to this family.",
        "\nStart by moving the {{lb:basket}} to {{lb:~}}. "
        "Use the command {{yb:mv basket ~/}}\n"
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
        "{{rb:Use the command}} {{yb:mv basket ~/}} "
        "{{rb:to move the}} {{lb:basket}} {{rb:to the windy road}} {{lb:~}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "Now follow the basket.  Use {{yb:cd}} by itself "
        "to go to the windy road Tilde.\n"
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~"
    commands = [
        "cd",
        "cd ~",
        "cd ~/"
    ]
    hints = [
        "{{rb:Use the command}} {{yb:cd}} {{rb:by itself "
        "to move yourself to the road ~}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "You are now back on the long windy road.  Look around you "
        "with {{yb:ls}} to check that you have your basket with you.\n"
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
        "ls"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:by itself "
        "to look around.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "You have your basket safely alongside you, and "
        "you see {{lb:my-house}} close by.",
        "Move the {{lb:basket}} to {{lb:my-house/kitchen}}.",
        "Don't forget to use the TAB key to autocomplete your commands.\n"
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
        "{{rb:Use}} {{yb:mv basket my-house/kitchen/}} "
        "{{rb:to move the basket to your kitchen.}}",
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Now go into {{lb:my-house/kitchen}} using {{lb:cd}}.\n",
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
        "{{rb:Use}} {{yb:cd my-house/kitchen/}} "
        "{{rb:to go to your kitchen.}}",
    ]
    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextStep(self.xp)
