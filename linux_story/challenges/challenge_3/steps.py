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
from linux_story.file_functions import write_to_file


class StepTemplateCat(Step):
    challenge_number = 3

    def __init__(self):
        Step.__init__(self, TerminalCat)


class Step1(StepTemplateCat):
    story = [
        "{{gCongratulations, you earned 5 XP!}}\n",
        "Love it! Put it on quickly.",
        "There's loads more interesting stuff in your room.",
        "Let's look in your {{yshelves}} using {{yls}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls shelves", "ls shelves/"]
    hints = "{{rType}} {{yls shelves}} {{rto look at your books.}}"

    def next(self):
        Step2()


class Step2(StepTemplateCat):
    story = [
        "That comic book looks fun. Take a look inside with {{ycat shelves/comic-book}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat shelves/comic-book"
    hints = "{{rType}} {{ycat shelves/comic-book}} {{rto read the comic.}}"

    def next(self):
        Step3()


class Step3(StepTemplateCat):
    story = [
        "Why is it covered in pawprints?",
        "Hang on, there's a note amongst your books.",
        "Read the note using {{ycat}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat shelves/note"
    hints = "{{rType}} {{ycat shelves/note}} {{rto read the note.}}"

    last_step = True
    challenge_number = 3

    def next(self):
        write_to_file("challenge", "4")
        NextChallengeStep()
