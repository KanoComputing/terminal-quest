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
from linux_story.challenges.challenge_13.c.steps import Step1 as NextStep
from linux_story.file_data import HIDDEN_DIR


class StepTemplateMv(Step):
    challenge_number = 12

    def __init__(self):
        Step.__init__(self, TerminalMv)


# Thanks you for saving the little girl
class Step1(StepTemplateMv):
    story = [
        "{{wb:Edith:}} Thank you for saving her!",
        "{{wb:Eleanor:}} Doggy!",
        "{{wb:Edith:}} Can you save her dog too?  I'm worried something will "
        "happen to it if it stays outside"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "mv ../dog .",
        "mv ../dog ./",
        "mv ~/town/dog ~/town/.hidden-shelter",
        "mv ~/town/dog ~/town/.hidden-shelter/",
        "mv ~/town/dog .",
        "mv ~/town/dog ./",
        "mv ../dog ~/town/.hidden-shelter",
        "mv ../dog ~/town/.hidden-shelter/",
    ]
    hints = [
        "{{rn:Use the command}} {{yb:mv ../dog .}}"
    ]
    dog_file = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/dog')
    counter = 0

    def __init__(self):
        self.save_fork('b')
        StepTemplateMv.__init__(self)

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

    '''def check_command(self, line, current_dir):

                    # strip any spaces off the beginning and end
                    line = line.strip()

                    if os.path.exists(self.dog_file) and self.counter < 3:
                        return True

                    # We can't verify the girl has been moved correctly at this step
                    elif line.strip() in self.command and self.counter == 3:
                        return True

                    elif self.counter == 3:
                        return True

                    else:
                        self.show_hint(line, current_dir)
                        return False'''

    def show_hint(self, line, current_dir):
        self.counter += 1
        StepTemplateMv.show_hint(self, line, current_dir)

    def next(self):
        if os.path.exists(self.dog_file):
            NextStep()
