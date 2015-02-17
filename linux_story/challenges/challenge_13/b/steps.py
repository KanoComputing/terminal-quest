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


# You save the little girl, but lose the dog.
class Step1(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{wn:Oh thank goodness I have you back safely.}}",
        "{{wb:Eleanor:}} {{wn:I lost my Doggie!!!}}",
        "{{wb:Edith:}} {{wn:I know I know, there's nothing we could do "
        "about that.}}",
        "{{wb:Edward:}} {{wn:Thank you so much for saving our little "
        "girl.}}\n",
        "{{gb:Well done for saving the little girl.}}",
        "Ask the people if there's anything else you can do to help."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = "cat Edward"
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} \"Thank you so much!  Eleanor, don't "
        "run outside again.\"",
        "cat Eleanor": "\n{{wb:Eleanor:}} \"Where has my dog gone?  Can you "
        "find him and bring him back?\""
    }
    hints = [
        "{{r:Edward looks like he has something to say.  Talk to him using "
        "{{yb:cat}}}}"
    ]

    def __init__(self):
        self.save_fork('b')
        StepTemplateMv.__init__(self)

    def show_hint(self, line, current_dir):
        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            self.send_hint(hint)
        else:
            StepTemplateMv.show_hint(self, line, current_dir)

    # Change this so we can cat everyone and see how they respond
    def next(self):
        NextStep()
