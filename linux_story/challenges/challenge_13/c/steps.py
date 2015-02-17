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


# Save both the dog and the little girl
class Step1(StepTemplateMv):
    story = [
        "{{wb:Eleanor:}} Yay, Doggie!",
        "{{wb:Dog:}} Ruff.",
        "{{wb:Edith:}} Oh thank goodness you got them both back.",
        "I was wrong about you. You're clearly a good person.\n",
        "{{gb:Awesome!  You're a hero!}}",
        "Talk to everyone and see if there's anything else you can do to "
        "help further"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = "cat Edward"
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} \"Thank you so much!  Eleanor, don't "
        "wander outside again.\"",
        "cat Eleanor": "\n{{wb:Eleanor}} \"Where do you think the bell would "
        "have taken us?\"",
        "cat dog": "\n{{wb:dog}} \"Woof! Woof woof!\""
    }
    hints = [
        "{{r:Edward looks like he has something he wants to say. "
        "Talk to Edward with}} {{yb:cat}}"
    ]
    last_step = True

    def __init__(self):
        self.save_fork('c')
        StepTemplateMv.__init__(self)

    def show_hint(self, line, current_dir):
        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            self.send_hint(hint)
        else:
            StepTemplateMv.show_hint(self, line, current_dir)

    def next(self):
        NextStep()
