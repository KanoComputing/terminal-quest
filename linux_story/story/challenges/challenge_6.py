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
from linux_story.story.challenges.challenge_7 import Step1 as NextChallengeStep
from linux_story.step_helper_functions import unblock_command_list


class StepTemplateCd(Step):
    challenge_number = 6

    def __init__(self, xp=""):
        Step.__init__(self, TerminalCd, xp)


class Step1(StepTemplateCd):
    story = [
        "Let Mum know about Dad. Type {{yb:cat Mum}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "cat Mum"
    hints = (
        "{{rb:To talk to your Mum, type}} {{yb:cat Mum}} {{rb:and press "
        "Enter}}."
    )

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "{{wb:Mum:}} {{Bn:\"You couldn't find him? That's strange, "
        "he wouldn't leave home without telling me first.\"",
        "\"Maybe he went to that town meeting with the Mayor,"
        " the one they were talking about on the news. "
        "Why don't you go and check? I'll stay here in case he comes "
        "back.\"}}\n",
        "Let's head to town. To leave the house, use {{yb:cd}} by itself"
    ]
    start_dir = "kitchen"
    end_dir = "~"
    command = ""
    hints = "{{rb:Type}} {{yb:cd}} {{rb:to start the journey.}}"

    def block_command(self, line):
        allowed_commands = ["cd"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "You're out of the house and on a long windy road called Tilde.",
        "Sometimes it is represented by the symbol ~"
        "Look around again to see where to go next."
    ]
    start_dir = "~"
    end_dir = "~"
    command = "ls"
    hints = "{{rb:Stuck?  Type}} {{yb:ls}} {{rb:to look around.}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "You can see a {{yb:town}} in the distance! Let's go there using "
        "{{yb:cd}}."
    ]
    start_dir = "~"
    end_dir = "town"
    command = ""
    hints = "{{rb:Type}} {{yb:cd town}} {{rb:to walk into town.}}"

    last_step = True

    def block_command(self, line):
        allowed_commands = ["cd town", "cd town/"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        NextChallengeStep(self.xp)
