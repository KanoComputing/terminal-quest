#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
# from linux_story.story.challenges.challenge_32 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 31


class Step1(StepTemplateNano):
    story = [
        "Huh, you can't see Bernard anywhere.",
        "I wonder where he went.",
        "Let's see what he was hiding in the secret room."
    ]
    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop/secret-room"
    commands = [
        "cd secret-room/",
        "cd secret-room"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(self.last_user_input, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Look around."
    ]
    start_dir = "~/town/east-part/shed-shop/secret-room"
    end_dir = "~/town/east-part/shed-shop/secret-room"
    commands = [
        "ls",
        "ls -a"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "You see what looks like a command, a diary, and a script.",
        "Examine them."
    ]
    start_dir = "~/town/east-part/shed-shop/secret-room"
    end_dir = "~/town/east-part/shed-shop/secret-room"
    commands = [
        "cat "
    ]
