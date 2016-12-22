#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

# Redo chapter 5 with the swordmaster.

import os

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.challenges.challenge_39 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateChmod(TerminalChmod):
    challenge_number = 38


class Step1(StepTemplateChmod):
    story = [
        "{{gb:You've found the answer to the swordmaster's riddle!}}",
        "Now {{lb:go back to the swordmaster's clearing.}}",
        ""
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/clearing"
    hints = [
        "Head back to the {{lb:~/woods/clearing}} where the swordmaster lives"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Knock on the swordmaster's door."
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo knock knock"
    ]
    hints = [
        "Use {{yb:echo knock knock}} to knock on the swordmaster's door"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Swordmaster:",
        "{{Bb:If you have me, you want to share me.",
        "If you share me, you haven't got me.",
        "What am I?}}",
        "",
        "{{yb:1. A secret}}",
        "{{yb:2. I don't know}}",
        "",
        "Use {{lb:echo}} to reply."
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo 1"
    ]
    hints = [
        "Swordmaster: {{lb:Incorrect. Did you finish the challenges in the cave? The answer was in there.}}"
    ]

    def next(self):
        path = self.generate_real_path("~/woods/clearing/house")
        os.chmod(path, 0755)
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "{{wb:Clunck.}} {{gb:It sounds like the door unlocked.}}",
        "",
        "{{lb:Go in the house.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:cd house}} {{rb:to go inside}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to go inside}}"
    ]
    commands = [
        "ls"
    ]

    def next(self):
        NextStep()