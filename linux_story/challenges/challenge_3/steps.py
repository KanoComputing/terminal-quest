#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
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


class StepTemplateCat(Step):
    challenge_number = 3

    def __init__(self):
        Step.__init__(self, TerminalCat)


class Step1(StepTemplateCat):
    story = [
        "{{gb:Congratulations, you earned 5 XP!}}\n",
        "Love it! Put it on quickly.",
        "There's loads more interesting stuff in your room.",
        "Let's look in your {{yb:shelves}} using {{yb:ls}}"
    ]
    start_dir = "my-room"
    end_dir = "my-room"
    command = ["ls shelves", "ls shelves/"]
    hints = "{{rb:Type}} {{yb:ls shelves}} {{rb:to look at your books.}}"

    def next(self):
        Step2()


class Step2(StepTemplateCat):
    story = [
        "That comic book looks fun. Take a look inside with "
        "{{yb:cat shelves/comic-book}}"
    ]
    start_dir = "my-room"
    end_dir = "my-room"
    command = "cat shelves/comic-book"
    hints = "{{rb:Type}} {{yb:cat shelves/comic-book}} {{rb:to read the comic.}}"

    def next(self):
        Step3()


class Step3(StepTemplateCat):
    story = [
        "Why is it covered in pawprints?",
        "Hang on, there's a {{yb:note}} amongst your books.",
        "Read the note using {{yb:cat}}"
    ]
    start_dir = "my-room"
    end_dir = "my-room"
    command = "cat shelves/note"
    hints = "{{rb:Type}} {{yb:cat shelves/note}} {{rb:to read the note.}}"

    last_step = True
    challenge_number = 3

    def next(self):
        NextChallengeStep()
