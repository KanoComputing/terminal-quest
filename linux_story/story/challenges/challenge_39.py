#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.challenges.challenge_40 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 39


class Step1(StepTemplateChmod):
    story = [
        "There's a file in this directory called RUN-ME. Read it."
    ]
    start_dir = "~/woods/clearing/house/no-entry-room"
    end_dir = "~/woods/clearing/house/no-entry-room"
    commands = [
        "cat RUN-ME"
    ]
    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:cat RUN-ME}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:This file contains code. However we can't run it until it's been made}} {{lb:executable}}",
        "{{Bb:Use}} {{lb:chmod +x RUN-ME}}"
    ]
    start_dir = "~/woods/clearing/house/no-entry-room"
    end_dir = "~/woods/clearing/house/no-entry-room"
    commands = [
        "chmod +x RUN-ME"
    ]
    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:chmod +x RUN-ME}}"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Look around to see how the file has changed.}}"
    ]
    start_dir = "~/woods/clearing/house/no-entry-room"
    end_dir = "~/woods/clearing/house/no-entry-room"
    commands = [
        "ls",
        "ls .",
        "ls ./",
        "ls -a",
        "ls -a .",
        "ls -a ./"
    ]
    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:ls}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Notice how the activated file has become}} {{gb:bright green}}{{Bb:?}}",
        "{{Bb:This means you can run the script. Use}} {{yb:./RUN-ME}} {{Bb:to run the script.}}"
    ]
    start_dir = "~/woods/clearing/house/no-entry-room"
    end_dir = "~/woods/clearing/house/no-entry-room"
    commands = [
        "./RUN-ME"
    ]
    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:./RUN-ME}}"
    ]

    def next(self):
        NextStep()
