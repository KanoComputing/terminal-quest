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
from linux_story.story.challenges.challenge_14 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_command_list


class StepTemplateMv(Step):
    challenge_number = 13

    def __init__(self):
        Step.__init__(self, TerminalMv)


class Step1(StepTemplateMv):
    story = [
        "{{gb:Congratulations, you earned 35 XP!}}\n",
        "{{wb:Edward:}} {{Bb:\"Hey, since you don't seem to be affected by "
        "going outside, can you gather some food for us?  We didn't have "
        "time to grab any before we went into hiding.\"",
        "\"Do you remember seeing any food in your travels?\"}}",
        "\n...ah! You have all that food in your {{yb:kitchen}}! "
        "We could give that to this family.",
        "\nStart by moving the {{yb:basket}} to {{yb:~}}. "
        "Use the command {{yb:mv basket ~}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "mv basket ~",
        "mv basket/ ~",
        "mv basket ~/",
        "mv basket/ ~/",
        "mv basket ../..",
        "mv basket/ ../..",
        "mv basket ../../",
        "mv basket/ ../../"
    ]
    hints = [
        "{{rb:Use the command}} {{yb:mv basket ~}} "
        "{{rb:to move the basket to the road ~.}}"
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "Now follow the basket.  Use {{yb:cd}} by itself "
        "to go to the road ~"
    ]
    start_dir = ".hidden-shelter"
    end_dir = "~"
    command = [
        "cd",
        "cd ~",
        "cd ~/"
    ]
    hints = [
        "{{rb:Use the command}} {{yb:cd}} {{rb:by itself "
        "to move yourself to the road ~}}"
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "You are now on a long windy road.  Look around you "
        "with {{yb:ls}} to check that you have your basket with you"
    ]

    start_dir = "~"
    end_dir = "~"
    command = [
        "ls"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:by itself"
        "to look around}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "You have your basket safely alongside you, and "
        "you see my-house close by.",
        "Move the {{yb:basket}} to {{yb:my-house/kitchen}}",
    ]

    start_dir = "~"
    end_dir = "~"
    command = [
        "mv basket my-house/kitchen",
        "mv basket/ my-house/kitchen",
        "mv basket my-house/kitchen/",
        "mv basket/ my-house/kitchen/",
        "mv basket ~/my-house/kitchen",
        "mv basket/ ~/my-house/kitchen",
        "mv basket ~/my-house/kitchen/",
        "mv basket/ ~/my-house/kitchen/"
    ]
    hints = [
        "{{rb:Use}} {{yb:mv basket my-house/kitchen/}} "
        "{{rb:to move the basket to your kitchen}}",
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Now go into {{yb:my-house/kitchen}} using {{yb:cd}}",
    ]

    start_dir = "~"
    end_dir = "kitchen"
    command = [
        "cd my-house/kitchen",
        "cd my-house/kitchen/",
        "cd ~/my-house/kitchen",
        "cd ~/my-house/kitchen/"
    ]
    hints = [
        "{{rb:Use}} {{yb:cd my-house/kitchen/}} "
        "{{rb:to go to your kitchen}}",
    ]
    last_step = True

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        NextStep()
