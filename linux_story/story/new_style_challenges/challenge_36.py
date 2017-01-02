#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.IStep import IStep
from linux_story.step_helper_functions import unblock_cd_commands, unblock_commands
from linux_story.story.new_terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(IStep):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "The bird flew out of the cage.",
        "According to the bird, we need to {{lb:move}} the {{lb:lighter}} from the {{lb:cage}} into the "
        "{{lb:locked-room.}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "mv cage/lighter locked-room/",
        "mv cage/lighter locked-room"
    ]
    hints = [
        "{{rb:Use}} {{yb:mv cage/lighter locked-room}} {{yb:to move the lighter to the locked-room}}"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 36, 2


class Step2(StepTemplateChmod):
    story = [
        "Go inside the {{bb:locked-room}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave/locked-room"

    hints = [
        "{{rb:Use}} {{yb:cd locked-room/}} {{rb:to go inside the locked-room.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 36, 3


class Step3(StepTemplateChmod):
    story = [
        "Activate the lighter with {{yb:chmod +x lighter}}"
    ]
    start_dir = "~/woods/cave/locked-room"
    end_dir = "~/woods/cave/locked-room"
    commands = [
        "chmod +x lighter"
    ]

    def next(self):
        return 36, 4


class Step4(StepTemplateChmod):
    story = [
        "Look around to see what happened to the lighter."
    ]

    start_dir = "~/woods/cave/locked-room"
    end_dir = "~/woods/cave/locked-room"

    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        return 36, 5


class Step5(StepTemplateChmod):
    story = [
        "The lighter went {{gb:bright green}} after you activated it.",
        "Now use it with {{yb:./lighter}}"
    ]
    start_dir = "~/woods/cave/locked-room"
    end_dir = "~/woods/cave/locked-room"

    commands = [
        "./lighter"
    ]

    def next(self):
        return 37, 1
