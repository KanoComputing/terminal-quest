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
from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_10 import Step1 as NextStep
from linux_story.helper_functions import play_sound
from linux_story.step_helper_functions import unblock_command_list


class StepTemplateCd(Step):
    challenge_number = 9

    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gb:Congratulations, you earned 25 XP!}}\n",
        "Oh no! Check your Mum is alright.",
        "Type {{yb:cd ..}} to leave town."
    ]
    start_dir = "town"
    end_dir = "~"
    command = ""
    hints = "{{rb:Use}} {{yb:cd ..}} {{rb:to progress.}}"

    def block_command(self, line):
        allowed_commands = ["cd ..", "cd ../"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        play_sound('bell')
        Step2()


class Step2(StepTemplateCd):
    story = [
        "{{pb:Ding. Dong.}}\n",
        "Type {{yb:cd my-house/kitchen}} to go straight to the kitchen"
    ]
    start_dir = "~"
    end_dir = "kitchen"
    command = ""
    hints = "{{rb:Use}} {{yb:cd my-house/kitchen}} {{rb:to go to the kitchen.}}"
    story_dict = {
        "Mum": {
            "exists": False
        }
    }

    def block_command(self, line):
        allowed_commands = ["cd my-house/kitchen", "cd my-house/kitchen/"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Check if everything is where it should be. Look around."
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "ls"
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to see that everything is where it "
        "should be.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Oh no - Mum's vanished too.",
        "Wait - there's another note.",
        "Use {{yb:cat}} to read the note."
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "cat note"
    hints = "{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}"
    last_step = True
    story_dict = {
        "Eleanor, Edward, Edith, apple": {
            "path": "~/town/.hidden-shelter",
        },
        "basket": {
            "directory": True,
            "path": "~/town/.hidden-shelter",
        },
        "empty-bottle": {
            "path": "~/town/.hidden-shelter"
        }
    }

    def next(self):
        NextStep()
