#!/usr/bin/env python
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
import time
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateChmod(TerminalChmod):
    challenge_number = 42



class Step1(StepTemplateChmod):
    story = [
        "The command locked away has been stolen...",
        "...",
        "What should you do now?",
    ]

    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "The swordsmaster appears.",
        "Swordsmaster: {{Bb:I felt something shift...did you get the command?}}",
        "",
        "{{yb:1: A white rabbit stole the command.}}",
        "{{yb:2: Yeah I got it. Nothing else happened.}}",
        "{{yb:3: Please don't kill me.}}"
    ]

    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    pass




