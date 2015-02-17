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
        "{{wb:Edward:}} Hey, that contains the information about the mv command you taught me",
        "I wonder where it came from?",
        "\nMaybe it's worth looking back in your house for more hidden items.",
        "To quickly go back home, use {{yb:cd ~/my-house/}}"
    ]

    start_dir = ".hidden-shelter"
    end_dir = "my-house"
    command = [
        'cd ~/my-house/',
        'cd ~/my-house'
    ]
    hints = [
        'No shortcuts!  Use {{yb:cd~/my-house}} to get back to your house'
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "Now, you need to look round your house for some hidden files.",
        "Where do you think they could be?"
    ]

    start_dir = 'my-house'

    def check_output(self, output):
        # Need to check that .chest is shown in the output of the command
        if '.chest' in output:
            return True

        return False

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "You found an old antique chest hidden under your bed",
        "You don't remember seeing it before",
        "Have a look inside the chest and see what it contains"
    ]

    start_dir = "my-room"
    end_dir = "my-room"

    def check_output(self, output):
        if 'ls' in output and 'cd' in output:
            return True

        return False

    def next(self):
        Step6()


class Step6(StepTemplateMv):
    story = [
        "You've found some rolls of paper, similar to what you found in the "
        ".hidden-shelter",
        "Use {{yb:cat}} to have a look at them"
    ]

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        "You recognise these commands.",
        "Maybe you should move the one you found in the {{yb:.hidden-shelter}}"
        " to the chest",
        "See if you can move it into the {{yb:chest}}"
    ]

    commands = [
        "mv ~/town/.hidden-shelter/mv chest/",
        "mv ~/town/.hidden-shelter/mv chest",
        "mv ../../.hidden-shelter/mv chest/",
        "mv ../../.hidden-shelter/mv chest",
        "mv ~/town/.hidden-shelter/mv ~/my-house/my-room/chest/",
        "mv ~/town/.hidden-shelter/mv ~/my-house/my-room/chest"
    ]
    hints = [
        "Move the scrap of parchment (called {{yb:mv}}) from "
        "{{yb:~/town/.hidden-shelter}} to the {{yb:chest}}",
        "You want to use the command {{yb:mv ~/town/.hidden-shelter/mv "
        "chest/}}"
    ]

    def next(self):
        Step8()


class Step8(StepTemplateMv):
    story = [
        "Is there anything else in this chest?",
        "Check there is nothing hidden in here."
    ]

    hints = [
        "Use {{yb:ls -a chest}} to see if there are any hidden items in the "
        "chest"
    ]

    command = [
        "ls -a chest",
        "ls -a chest/"
    ]

    def next(self):
        Step9()


class Step9(StepTemplateMv):
    story = [
        "So someone left these for you to find?",
        "But who?"
        "TO BE CONTINUED"
    ]

    def next(self):
        self.exit()
