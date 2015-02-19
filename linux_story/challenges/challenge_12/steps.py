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
from linux_story.challenges.challenge_13.steps import Step1 as NextStep
from linux_story.file_data import HIDDEN_DIR
from linux_story.step_helper_functions import unblock_command_list


class StepTemplateMv(Step):
    challenge_number = 12

    def __init__(self):
        Step.__init__(self, TerminalMv)


# Thanks you for saving the little girl
class Step1(StepTemplateMv):
    story = [
        "{{gb:Congratulations, you earned 30 XP!}}\n",
        "{{wb:Edith:}} {{Bb:Thank you for saving her!}}",
        "{{wb:Eleanor:}} {{Bb:Doggy!}}",
        "{{wb:Edith:}} {{Bb:Can you save her dog too?  I'm worried something "
        "will happen to it if it stays outside.}}"
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
        "{{rb:Use the command}} {{yb:mv ../dog .}}"
    ]
    dog_file = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/dog')

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step2()


# Save both the dog and the little girl
class Step2(StepTemplateMv):
    story = [
        "{{wb:Eleanor:}} {{Bb:Yay, Doggie!}}",
        "{{wb:Dog:}} {{Bb:Ruff!}}",
        "{{wb:Edith:}} {{Bb:Oh thank goodness you got them both back.",
        "I was wrong about you. You're clearly a good person.}}\n",
        "{{gb:Awesome!  You're a hero!}}",
        "Talk to everyone and see if there's anything else you can do to "
        "help further."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = "cat Edward"
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} {{Bb:\"Thank you so much! "
        "Eleanor, don't wander outside again.\"}}",
        "cat Eleanor": "\n{{wb:Eleanor:}} {{Bb:\"Where do you think the "
        "bell would have taken us?\"}}",
        "cat dog": "\n{{wb:Dog:}} {{Bb:\"Woof! Woof woof!\"}}"
    }
    hints = [
        "{{ob:Edward looks like he has something he wants to say. "
        "Talk to Edward with}} {{yb:cat Edward}}"
    ]
    last_step = True

    def show_hint(self, line, current_dir):
        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            self.send_hint(hint)
        else:
            StepTemplateMv.show_hint(self, line, current_dir)

    def next(self):
        NextStep()
