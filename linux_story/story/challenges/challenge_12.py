# challenge_12.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_13 import Step1 as NextStep
from linux_story.common import tq_file_system
from linux_story.step_helper_functions import unblock_commands


class StepTemplateMv(TerminalMv):
    challenge_number = 12


# ----------------------------------------------------------------------------------------


# Thanks you for saving the little girl
class Step1(StepTemplateMv):
    story = [
        _("{{wb:Edith:}} {{Bb:\"Thank you for saving her!\"}}"),
        _("{{wb:Eleanor:}} {{Bb:\"Doggy!\"}}"),
        _("{{wb:Edith:}} {{Bb:\"Can you save her dog too? I'm worried something will happen to it if it stays outside.\"}}\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
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
        _("{{rb:Use the command}} {{yb:mv ../dog ./}} {{rb:to rescue the dog.}}")
    ]
    dog_file = os.path.join(tq_file_system, 'town/.hidden-shelter/dog')

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step2()


# Save both the dog and the little girl
class Step2(StepTemplateMv):
    story = [
        _("{{wb:Eleanor:}} {{Bb:\"Yay, Doggie!\"}}"),
        _("{{wb:Dog:}} {{Bb:\"Ruff!\"}}"),
        _("{{wb:Edith:}} {{Bb:\"Thank you so much for getting them both back."),
        _("I was wrong about you. You're a hero!\"}}\n"),
        _("{{lb:Listen to everyone}} and see if there's anything else you can do to help.\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = "cat Edward"
    all_commands = {
        "cat Edith": _("\n{{wb:Edith:}} {{Bb:\"Thank you so much! Eleanor, don't wander outside again - you scared the life out of me!\"}}"),
        "cat Eleanor": _("\n{{wb:Eleanor:}} {{Bb:\"Where do you think the bell would have taken us?\"}}"),
        "cat dog": _("\n{{wb:Dog:}} {{Bb:\"Woof! Woof woof!\"}}")
    }
    hints = [
        _("{{gb:Edward looks like he has something he wants to say. Listen to Edward with}} {{yb:cat Edward}}")
    ]
    last_step = True

    def show_hint(self):
        if self.last_user_input in self.all_commands.keys():
            hint = self.all_commands[self.last_user_input]
            self.send_hint(hint)
        else:
            # Show default hints.
            self.send_hint()

    def next(self):
        NextStep(self.xp)
