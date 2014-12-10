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
from linux_story.challenges.challenge_2.terminals import TerminalCat
from linux_story.challenges.challenge_4.steps import Step1 as NextChallengeStep
from linux_story.file_data import copy_data
from linux_story.file_functions import write_to_file


class StepTemplateCat(Step):
    def __init__(self):
        Step.__init__(self, TerminalCat)


class Step1(StepTemplateCat):
    story = [
        "Your mum is calling you! Better get dressed...",
        "Type {{yls wardrobe}} to find something to wear"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls wardrobe", "ls wardrobe/"]
    hints = "Type {{yls wardrobe}} to find something to wear"

    def next(self):
        Step2()


class Step2(StepTemplateCat):
    story = [
        "Type {{ycat wardrobe/hat}} to see how it looks"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat wardrobe/hat"
    hints = "Type {{ycat wardrobe/hat}} to find something to wear"

    def next(self):
        Step3()


class Step3(StepTemplateCat):
    story = [
        "Love it! Put it on quickly.",
        "Hang on, there's a note on your desk...",
        "Type {{ycat note}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat note"
    hints = "Type {{ycat note}} to read what's on your computer"

    def next(self):
        copy_data(4)
        write_to_file("challenge", "4")
        NextChallengeStep()
