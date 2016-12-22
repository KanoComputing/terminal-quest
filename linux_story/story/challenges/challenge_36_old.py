#!/usr/bin/env python
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.challenges.challenge_37_old import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 36


class Step1(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:This file has also had its read permissions removed. This means you cannot read the "
        "contents of the file.}}",
        "{{Bb:Repeat what you did to make the file readable.}}"

    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "chmod +r dark-room/READ-ME",
    ]
    hints = [
        "Swordmaster: {{Bb:Press UP a few times on the keyboard if you don't remember what you typed..}}",
        "Swordmaster: {{Bb:Try typing}} {{yb:chmod +r dark-room/READ-ME}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:Now read the file.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        # Congratulation, you learnt how to make things readable.
        # Could be a hint for something to come?
        # Could be something he found?
        "cat dark-room/READ-ME"
    ]
    hints = [
        "Swordmaster: {{Bb:Use}} {{yb:cat dark-room/READ-ME}}"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:You can also remove the permissions. If you use}}",
        "{{yb:chmod -r dark-room}}",
        "{{Bb:you will be unable to look inside.}}",
        "{{Bb:Try it!}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    commands = [
        "chmod -r dark-room",
        "chmod -r dark-room/"
    ]

    hints = [
        "Swordmaster: {{Bb:Use}} {{yb:chmod -r dark-room}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:Look inside to confirm you cannot see inside.}}"
    ]

    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    commands = [
        "ls dark-room",
        "ls dark-room/",
        "ls dark-room/READ-ME"
    ]

    hints = [
        "Swordmaster: {{Bb:Use}} {{yb:ls dark-room}}"
    ]

    def next(self):
        NextStep()
