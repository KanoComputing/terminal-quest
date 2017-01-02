#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.challenges.challenge_39_old import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 38


class Step1(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:Try and go into the}} {{bb:no-entry-room}}",
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    dirs_to_attempt = "~/woods/clearing/house/no-entry-room"
    commands = [
        "cd no-entry-room",
        "cd no-entry-room/"
    ]
    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:cd no-entry-room}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:You are blocked from going inside. This is because the}} {{lb:execute}} {{Bb:permission "
        "has been removed from this room.}}",
        "{{Bb:Use}} {{yb:chmod +x no-entry-room}} {{Bb:to allow yourself to go inside.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    dirs_to_attempt = "~/woods/clearing/house/no-entry-room"
    commands = [
        "chmod +x no-entry-room",
        "chmod +x no-entry-room/"
    ]
    hints = [
        "Swordmaster: {{Bb:Use}} {{yb:chmod +x no-entry-room}}"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Now try and go inside"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house/no-entry-room"
    commands = [
        "cd no-entry-room",
        "cd no-entry-room/"
    ]
    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:cd no-entry-room}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Look around"
    ]
    start_dir = "~/woods/clearing/house/no-entry-room"
    end_dir = "~/woods/clearing/house/no-entry-room"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]
    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:ls}}"
    ]

    def next(self):
        NextStep()
