#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.terminals.terminal_nano import TerminalNano
# from linux_story.story.challenges.challenge_28 import Step1 as NextChallengeStep


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 27


class StepTemplateNano(TerminalNano):
    challenge_number = 27


class Step1(StepTemplateMkdir):
    story = [
        "You are back in the shed-maker's place.",
        "Have a look around."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    commands = [
        "ls",
        "ls -a"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Bernard: {{Bb:Hellooooo. You came back to fix my script!}}",

        "Let's see whether we can fix it.",

        "Let's try and use {{yb:nano best-horn-in-the-world}} to "
        "edit it."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    commands = [
        "nano best-horn-in-the-world"
    ]

    hints = [
        "{{rb:Use}} {{yb:nano best-horn-in-the-world}} "
        "{{rb:to edit the tool.}}"
    ]

    nano_end_content = "echo HONK!"
    nano_filepath = "~/town/east-part/best-horn-in-the-world.sh"

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "{{gb:Yessssssss you passed.}}"
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    def next(self):
        pass
