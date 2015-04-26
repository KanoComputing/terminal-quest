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
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_17 import Step1 as NextChallengeStep
from linux_story.step_helper_functions import unblock_commands
import time


class StepTemplateMv(Step):
    challenge_number = 16

    def __init__(self, xp=""):
        Step.__init__(self, TerminalMv, xp)


class Step1(StepTemplateMv):
    story = [
        "There is an old antique chest hidden under your bed, "
        "which you don't remember seeing before.",
        "You walk into my-room to have a closer look.",
        "Peer inside the {{yb:.chest}} and see what it contains."
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    commands = [
        'ls .chest',
        'ls .chest/',
        'ls -a .chest',
        'ls -a .chest/',
        'ls .chest/ -a',
        'ls .chest -a'
    ]

    hints = [
        "{{rb:Use}} {{yb:ls .chest}} {{rb:to look inside the .chest}}"
    ]

    def check_output(self, output):
        if not output:
            return False

        if 'ls' in output and 'cd' in output:
            return True

        return False

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "There are some rolls of parchment, similar to what you found in "
        "the .hidden-shelter",
        "Use {{yb:cat}} to read one of the scrolls"
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    commands = [
        'cat .chest/LS',
        'cat .chest/CAT',
        'cat .chest/CD'
    ]

    hints = [
        "{{rb:Use}} {{yb:cat .chest/LS}} {{rb:to read the LS scroll}}"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "You recognise these commands.",
        "Maybe you should {{yb:move}} the one you found in the "
        "{{yb:~/town/.hidden-shelter/.tiny-chest}} to this {{yb:.chest}}, "
        "so they're all safe and in the same place.",
        "\n{{gb:Use the TAB key to complete the file paths - it will save you "
        "typing!}}"
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    commands = [
        "mv ~/town/.hidden-shelter/.tiny-chest/MV .chest/",
        "mv ~/town/.hidden-shelter/.tiny-chest/MV .chest",
        "mv ../../.hidden-shelter/.tiny-chest/MV .chest/",
        "mv ../../.hidden-shelter/.tiny-chest/MV .chest",
        "mv ~/town/.hidden-shelter/.tiny-chest/MV ~/my-house/my-room/.chest/",
        "mv ~/town/.hidden-shelter/.tiny-chest/MV ~/my-house/my-room/.chest"
    ]
    hints = [
        "{{rb:You want to use the command}} "
        "{{yb:mv ~/town/.hidden-shelter/.tiny-chest/MV .chest/}}"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "I wonder if theres anything else hidden in this {{yb:.chest}}?",
        "Have a closer look for some more items."
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    hints = [
        "{{rb:Use}} {{yb:ls -a .chest}} {{rb:to see if there are any "
        "hidden items in the chest}}"
    ]

    commands = [
        "ls -a .chest",
        "ls -a .chest/",
        'ls .chest/ -a',
        'ls .chest -a'
    ]

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "You suddenly notice a tiny stained {{yb:.note}}, scrumpled in "
        "the corner of the {{yb:.chest}}",
        "What does it say?"
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    hints = [
        "{{rb:Use}} {{yb:cat .chest/.note}} {{rb:to read the}} {{yb:.note}}"
    ]

    commands = [
        "cat .chest/.note"
    ]

    def next(self):
        NextChallengeStep(self.xp)

        # self.exit()

        # So that server has time to send message before it closes
        # time.sleep(3)
