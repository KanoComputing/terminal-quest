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
from linux_story.story.challenges.challenge_16 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_command_list


class StepTemplateMv(Step):
    challenge_number = 15

    def __init__(self, xp=""):
        Step.__init__(self, TerminalMv, xp)


class Step1(StepTemplateMv):
    story = [
        "What was that spell that helped you find these hidden townsfolk? "
        "you should try that again to make sure theres nothing you've overlooked!"
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
        "What's that! There's {{yb:.tiny-chest}} in the corner of the shelter",
        "\n{{wb:Edward:}} {{Bb:\"Hey, what's that doing there? "
        "Has it been there all along? Why couldn't I see it?\"}}",
        "\nHave a look inside the {{yb:.tiny-chest}}"
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
        "You see a scroll of parchment inside, with a stamp on it saying "
        "{{yb:MV}}.",
        "Read what it says."
    ]

    hints = [
        "{{rb:Use}} {{yb:cat .tiny-chest/MV}} {{rb:to read the MV parchment}}"
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
        "{{wb:Edward:}} {{Bb:\"Hey, that contains information about the "
        "mv command you taught me. Why is it here?",
        "I wonder where it came from?\"}}",
        "\nMaybe you should go back to {{yb:my-house}} to see if you can find any more of these hidden items.",
        "To quickly go back home, use {{yb:cd ~/my-house/}}"
    ]

    start_dir = ".hidden-shelter"
    end_dir = "my-house"
    command = [
        'cd ~/my-house/',
        'cd ~/my-house'
    ]
    hints = [
        '{{rb:No shortcuts!  Use}} {{yb:cd ~/my-house}} '
        '{{rb:to get back to your house in one step}}'
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Let's see if we can find anything hidden around here!",
        "Where do you think any hidden things could be?"
    ]

    start_dir = 'my-house'

    hints = [
        "{{gb:Have a look in all the places of my-house using}} {{yb:ls -a}}",
        "{{gb:Have a look in all the places of my-house using}} {{yb:ls -a}}",
        "{{gb:Have a look in all the places of my-house using}} {{yb:ls -a}}",
        "{{rb:Stuck?  Have a look in}} {{yb:my-room}}",
        "{{rb:Use}} {{yb:ls -a my-room}} {{rb:to look for hidden files in "
        "my-room}}"
    ]

    last_step = True

    def check_output(self, output):
        # Need to check that .chest is shown in the output of the command
        if not output:
            return False

        if '.chest' in output:
            return True

        return False

    def next(self):
        NextStep(self.xp)
