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
from linux_story.challenges.challenge_11.terminals import TerminalMv


class StepTemplateMv(Step):
    challenge_number = 14

    def __init__(self):
        Step.__init__(self, TerminalMv)


class Step1(StepTemplateMv):
    story = [
        "Before you go, have a look to see if there is anything you've "
        "overlooked",
        "Have a closer look at your surroundings"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls -a}} {{rb:to look more closely around you}}"
    ]

    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "ls -a"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "{{wb:Edward}} Hey, what's that?",
        "A {{yb:.note}} appeared in our shelter?",
        "Has it been there all along?",
        "What does it say?"
    ]

    hints = [
        "{{rb:Use}} {{yb:cat .note}} {{rb:to read the note}}"
    ]

    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "cat .note"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "{{wb:Edward:}} Who is that note from?",
        "Has our shelter been found?"
    ]

    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"

    def next(self):
        self.exit()
