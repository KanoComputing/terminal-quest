#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.challenges.challenge_37 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands, unblock_commands


class StepTemplateChmod(TerminalChmod):
    challenge_number = 36


class Step1(StepTemplateChmod):
    story = [
        "The bird flew out of the cage.",
        "According to the bird, we need to {{lb:move the lighter from the cage into the locked-room.}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "mv cage/lighter locked-room/",
        "mv cage/lighter locked-room"
    ]
    hints = [
        "Use {{yb:mv cage/lighter locked-room}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Go inside the {{bb:locked-room}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave/locked-room"

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Activate the lighter with {{yb:chmod +x lighter}}"
    ]
    start_dir = "~/woods/cave/locked-room"
    end_dir = "~/woods/cave/locked-room"

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Look around to see what happened to the lighter"
    ]

    start_dir = "~/woods/cave/locked-room"
    end_dir = "~/woods/cave/locked-room"

    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = [
        "The lighter went {{gb:bright green}} after you activated it.",
        "Now use it with {{yb:./lighter}}"
    ]
    start_dir = "~/woods/cave/locked-room"
    end_dir = "~/woods/cave/locked-room"

    hints = "To use the lighter, "

    commands = [
        "./lighter"
    ]

    def next(self):
        NextStep()