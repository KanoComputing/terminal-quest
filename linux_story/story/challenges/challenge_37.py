#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
import os

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.challenges.challenge_38 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 37


class Step1(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Well done. Your next challenge is the}} {{lb:Cage Room}}",
        "{{lb:Go inside}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house/cage-room"
    commands = [
        "cd cage-room",
        "cd cage-room/"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Look around"
    ]
    start_dir = "~/woods/clearing/house/cage-room"
    end_dir = "~/woods/clearing/house/cage-room"
    commands = [
        "ls"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "There's a bird inside.",
        "",
        "Swordsmaster: {{Bb:The bird can't escape, as the cage-room has had its}} {{lb:write}} {{Bb:permissions "
        "removed.}}",
        "{{Bb:To return the write permissions and allow the bird to escape, use}} {{yb:chmod +w ./}}"
    ]
    start_dir = "~/woods/clearing/house/cage-room"
    end_dir = "~/woods/clearing/house/cage-room"
    commands = [
        "chmod +w .",
        "chmod +w ./"
    ]

    def next(self):
        # alternatively, launch new window
        os.system("python /usr/bin/bird.py 1")
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "The bird flew away",
        "",
        "Swordmaster: {{Bb:I found that bird when it was injured. Now it's better it should be free.}}",
        "{{Bb:Come out and you will face your last challenge.}}"
    ]

    start_dir = "~/woods/clearing/house/cage-room"
    end_dir = "~/woods/clearing/house"
    commands = [
        "cd ..",
        "cd ../"
    ]
    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:cd ..}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep()

