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
from linux_story.step_helper_functions import unblock_command_list
import time


class StepTemplateMv(Step):
    challenge_number = 17

    def __init__(self):
        Step.__init__(self, TerminalMv)


class Step1(StepTemplateMv):
    story = [
        "{{gb:Congratulations, you earned 40 XP!}}\n",
        "You've found a strange hidden chest in your room.",
        "Could there be other objects in the other rooms?"
    ]

    start_dir = "my-room"
    # Don't check the end_dir?
    # But where do we start them off then?

    '''command = [
        'ls .chest',
        'ls .chest/',
        'ls -a .chest',
        'ls -a .chest/'
    ]'''

    hints = [
        "{{gb:Have a look in the other rooms}}"
    ]

    def check_output(self, output):

        # User needs to find their mum's safe
        if '.safe' in output:
            return True

        return False

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "You go into your Mum's room to check out the .safe",
        "What is in it?"
    ]

    start_dir = "parents-room"
    end_dir = "parents-room"
    command = ["ls .safe", "ls -a safe"]
    hints = "Look in the safe using ls"

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "You found a book in your Mum's room",
        "You know you're not supposed to read other people's diaries...",
        "What else is in here?"
    ]

    start_dir = "my-room"
    end_dir = "my-room"

    command = "cat ECHO"

    hints = [
        "{{rb:Use}} {{yb:cat .chest/LS}} {{rb:to read the LS scroll}}"
    ]

    def next(self):
        Step4()
