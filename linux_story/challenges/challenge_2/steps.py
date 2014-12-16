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
from terminals import TerminalCat
from linux_story.challenges.challenge_3.steps import Step1 as NextChallengeStep
#from linux_story.file_data import copy_data
from linux_story.file_functions import write_to_file


class StepTemplateCat(Step):
    def __init__(self):
        Step.__init__(self, TerminalCat)


class Step1(StepTemplateCat):
    story = [
        "Better turn that alarm off.",
        "\n{{wNew Spell}}: to look at objects, we type {{ycat}}."
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat alarm"
    hints = "Type {{ycat alarm}} to see the alarm."

    def next(self):
        Step2()


class Step2(StepTemplateCat):
    story = [
        "Ok - it's switched off. There's lots of other interesting things to look at - check them out!",
        "Have a look at your {{bshelves}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls shelves", "ls shelves/"]
    hints = "Type {{yls shelves}} to look at your books"

    def next(self):
        Step3()


class Step3(StepTemplateCat):
    story = [
        "That comic book looks fun. Take a look inside."
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat shelves/comic-book"
    hints = "Type {{ycat shelves/comic-book}} to read the comic."

    def next(self):
        #copy_data(3)
        write_to_file("challenge", "3")
        NextChallengeStep()
