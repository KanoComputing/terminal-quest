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
    challenge_number = 15

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
        "You notice a {{yb:.tiny-chest}} in the corner of the shelter",
        "\n{{wb:Edward}} \"Hey, what's that?",
        "There's a {{yb:.tiny-chest}} is in our shelter?",
        "Has it been there all along? What's in it?\""
    ]

    hints = [
        "{{rb:Use}} {{yb:ls .tiny-chest}} {{rb:to look inside}}"
    ]

    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "ls .tiny-chest",
        "ls .tiny-chest/",
        "ls -a .tiny-chest",
        "ls -a .tiny-chest/"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "You see a scroll of parchment inside, with a stamp on it saying {{wb:MV}}.",
        "Open it and read what it says."
    ]

    hints = [
        "{{rb:Use}} {{yb:cat .tiny-chest/MV}} {{rb:to read the note}}"
    ]

    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "cat .tiny-chest/MV"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "{{wb:Edward:}} \"Hey, that contains the information about the mv "
        "command you taught me",
        "I wonder where it came from?\"",
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
        '{{rb:No shortcuts!  Use}} {{yb:cd ~/my-house}} {{rb:to get back to your house}}'
    ]

    def block_command(self, line):
        if 'cd' in line and line.strip() not in self.command:
            return True

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Now, you need to look round your house for some hidden files.",
        "Where do you think they could be?"
    ]

    start_dir = 'my-house'

    hints = [
        "{{rb:Have a look in all the places of my-house using}} {{yb:ls -a}}"
    ]

    def check_output(self, output):
        # Need to check that .chest is shown in the output of the command
        if not output:
            return False

        if '.chest' in output:
            return True

        return False

    def next(self):
        Step6()


class Step6(StepTemplateMv):
    story = [
        "You find an old antique chest hidden under your bed",
        "You don't remember seeing it before",
        "You walk into my-room to have a closer look",
        "Have a look inside the {{yb:.chest}} and see what it contains"
    ]

    start_dir = "my-room"
    end_dir = "my-room"

    command = [
        'ls .chest',
        'ls .chest/',
        'ls -a .chest',
        'ls -a .chest/'
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
        Step7()


class Step7(StepTemplateMv):
    story = [
        "You've found some rolls of parchment, similar to what you found in "
        "the .hidden-shelter",
        "Use {{yb:cat}} to have a look at one of the scrolls"
    ]

    start_dir = "my-room"
    end_dir = "my-room"

    command = [
        'cat .chest/LS',
        'cat .chest/CAT',
        'cat .chest/CD'
    ]

    hints = [
        "{{rb:Use}} {{yb:cat}} {{rb:to look at a scroll}}",
        "{{rb:Use}} {{yb:cat .chest/LS}} {{rb:to read the LS scroll}}",
    ]

    def next(self):
        Step8()


class Step8(StepTemplateMv):
    story = [
        "You recognise these commands.",
        "Maybe you should move the one you found in the "
        "{{yb:.hidden-shelter/.tiny-chest}} to the {{yb:.chest}}"
    ]

    start_dir = "my-room"
    end_dir = "my-room"

    command = [
        "mv ~/town/.hidden-shelter/.tiny-chest/MV .chest/",
        "mv ~/town/.hidden-shelter/.tiny-chest/MV .chest",
        "mv ../../.hidden-shelter/.tiny-chest/MV .chest/",
        "mv ../../.hidden-shelter/.tiny-chest/MV .chest",
        "mv ~/town/.hidden-shelter/.tiny-chest/MV ~/my-house/my-room/.chest/",
        "mv ~/town/.hidden-shelter/.tiny-chest/MV ~/my-house/my-room/.chest"
    ]
    hints = [
        "{{rb:Move the scrap of parchment (called}} {{yb:MV}}{{rb:) from}} "
        "{{yb:~/town/.hidden-shelter/.tiny-chest}} {{rb:to the}} "
        "{{yb:.chest}}",

        "{{rb:You want to use the command}} "
        "{{yb:mv ~/town/.hidden-shelter/.tiny-chest/MV .chest/}}"
    ]

    def block_command(self, line):
        if 'mv' in line and line.strip() not in self.command:
            return True

    def next(self):
        Step9()


class Step9(StepTemplateMv):
    story = [
        "Is there anything else in this chest?",
        "Check there is nothing hidden in here."
    ]

    start_dir = "my-room"
    end_dir = "my-room"

    hints = [
        "Use {{yb:ls -a .chest}} to see if there are any hidden items in the "
        "chest"
    ]

    command = [
        "ls -a .chest",
        "ls -a .chest/"
    ]

    def next(self):
        Step10()


class Step10(StepTemplateMv):
    story = [
        "There's another {{yb:.note}} inside?",
        "What does it say?"
    ]

    start_dir = "my-room"
    end_dir = "my-room"

    hints = [
        "{{rb:Use}} {{yb:cat .chest/.note}} {{rb:to read the}} {{yb:.note}}"
    ]

    command = [
        "cat .chest/.note"
    ]

    def next(self):
        Step11()


class Step11(StepTemplateMv):
    story = [
        "So someone left these for you to find?",
        "But who?",
        "{{gb:TO BE CONTINUED}}"
    ]

    start_dir = "my-room"
    end_dir = "my-room"

    def next(self):
        self.exit()
