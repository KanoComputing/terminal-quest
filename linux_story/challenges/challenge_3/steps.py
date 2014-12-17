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
#from linux_story.file_data import copy_data
from linux_story.file_functions import write_to_file


class StepTemplateCat(Step):
    def __init__(self):
        Step.__init__(self, TerminalCat)

####################
# We expect people to trip up on this step.  More explanation needed?
class Step1(StepTemplateCat):
    story = [
        "{{gCongratulations, you earned 10 XP!}}\n",
        "Love it! Put it on quickly.",
        "There's loads more interesting stuff in your room.",
        "Let's look in your {{bshelves}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls shelves", "ls shelves/"]
    hints = "Type {{yls shelves}} to look at your books"

    def next(self):
        Step2()


class Step2(StepTemplateCat):
    story = [
        "That comic book looks fun. Take a look inside with {{ycat shelves/comic-book}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat shelves/comic-book"
    hints = "Type {{ycat shelves/comic-book}} to read the comic."

    def next(self):
        Step3()


class Step3(StepTemplateCat):
    story = [
        "Why is it covered in pawprints?",
        "Hang on, there's a note amongst your books",
        "Read the note using {{ycat}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat shelves/note"
    hints = "Type {{ycat shelves/note}} to read the note"

    def next(self):
        #copy_data(4)
        write_to_file("challenge", "4")
        NextChallengeStep()
