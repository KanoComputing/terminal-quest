#!/usr/bin/env python
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.challenges.challenge_36 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 35


class StepTemplateChmod(TerminalChmod):
    challenge_number = 35


class Step1(StepTemplateNano):
    story = [
        "Swordsmaster: {{Bb:See your name on everything in this house? You have extra permissions in this world, "
        "and the best chance of stopping people disappearing.}}",
        "{{Bb:I will teach you what you need to know, using three rooms to challenge you.}}",
        "{{Bb:We'll start with the}} {{lb:dark-room}}",
        "{{Bb:First}} {{lb:look inside}}",
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "ls dark-room",
        "ls dark-room/",
    ]
    hints = [
        "Swordsmaster: {{Bb:Remember how to look inside a room?}}",
        "Swordsmaster: {{Bb:I thought you were smart...}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:The lights in this room are off. To turn them on, you need to restore your}} "
        "{{lb:read}} {{Bb:permissions to the room.}}",
        "{{Bb:Use}} {{yb:chmod +r dark-room}} {{Bb:to turn the lights on.}}"
        # add new spell here of chmod +r
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "chmod +r dark-room",
        "chmod +r dark-room/"
    ]
    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:chmod +r dark-room}}"
    ]

    def next(self):
        Step3()



class Step3(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:You've added the read permissions. Now look inside.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "ls dark-room",
        "ls dark-room/",
    ]

    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:ls dark-room}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:You can see a note}} {{lb:READ-ME}} {{Bb:Read it.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "cat dark-room/READ-ME"
    ]

    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:cat dark-room/READ-ME}}"
    ]

    def next(self):
        NextStep()
