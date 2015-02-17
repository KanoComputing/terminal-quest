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

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.challenges.challenge_11.terminals import TerminalMv
from linux_story.challenges.challenge_14.steps import Step1 as NextStep


class StepTemplateMv(Step):
    challenge_number = 13

    def __init__(self):
        Step.__init__(self, TerminalMv)


# You lose both the dog and the little girl.
class Step1(StepTemplateMv):
    story = [
        "{{wb:Edith:}} I heard a bell!",
        "Check on my little girl!"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "ls ../",
        "ls ..",
        "ls ~/town",
        "ls ~/town/"
    ]
    hints = [
        "{{r:Use the command}} {{yb:ls ..}} {{rn:to look back a directory}}"
    ]

    def __init__(self):
        self.save_fork('a')
        StepTemplateMv.__init__(self)

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "{{wb:Edith:}} My little girl has gone! How could you let her get "
        "taken away like that??",
        "{{wb:Edward:}}  Oh, this is awful\n",
        "{{rn:You}} {{rb:failed}} {{rn:at your mission.}}\n",

        # To simplify the game, you could have a game over screen here
        "Talk to the people to see if you can make up for this."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = "cat Edward"
    hints = [
        "{{r:Edward looks like he has something to ask.  Talk to him}}",
        "{{r:Use}} {{yb:cat Edward}} {{rn:to talk to Edward}}"
    ]
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} \"Don't talk to me.\""
    }
    last_step = True

    def show_hint(self, line, current_dir):
        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            self.send_hint(hint)
        else:
            StepTemplateMv.show_hint(self, line, current_dir)

    def next(self):
        # When you talk to the correct person
        NextStep()
