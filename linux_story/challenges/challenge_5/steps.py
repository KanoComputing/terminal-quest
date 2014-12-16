#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.Step import Step
from linux_story.challenges.challenge_4.terminals import TerminalCd
from linux_story.file_functions import write_to_file


class StepTemplateCd(Step):
    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "Let's go and look for Dad.",
        "To go to the garden, type {{ycd garden}}"
    ]
    start_dir = "kitchen"
    end_dir = "garden"
    command = ""
    hints = "To go to the garden, type {{ycd garden}}"

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "You can use {{yls}} + {{ycat}} to take a look around,",
        "Type {{ycd greenhouse}} to go inside the greenhouse."
    ]
    start_dir = "garden"
    end_dir = "greenhouse"
    command = ""
    hints = "To go to the greenhouse, type {{ycd greenhouse}}"

    def next(self):
        write_to_file("exit")
