# challenge_12.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


# Change this import statement, need to decide how to group the terminals
# together
import os
from linux_story.StepTemplate import StepTemplate
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.common import tq_file_system
from linux_story.step_helper_functions import unblock_commands


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


# Thanks you for saving the little girl
class Step1(StepTemplateMv):
    story = [
        _("{{wb:Edith:}} {{Bb:\"Thank you for saving her!\"}}"),
        _("{{wb:Eleanor:}} {{Bb:\"Doggy!\"}}"),
        _("{{wb:Edith:}} {{Bb:\"Can you save her dog too? I'm worried something " +\
        "will happen to it if it stays outside.\"}}\n")
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

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 12, 2


# Save both the dog and the little girl
class Step2(StepTemplateMv):
    story = [
        _("{{wb:Eleanor:}} {{Bb:\"Yay, Doggie!\"}}"),
        _("{{wb:Dog:}} {{Bb:\"Ruff!\"}}"),
        _("{{wb:Edith:}} {{Bb:\"Thank you so much for getting them both back."),
        _("I was wrong about you. You're a hero!\"}}\n"),
        _("{{lb:Listen to everyone}} and see if there's anything else you can " +\
        "do to help.\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = "cat Edward"
    all_commands = {
        "cat Edith": _("\n{{wb:Edith:}} {{Bb:\"Thank you so much! " +\
        "Eleanor, don't wander outside again - you scared the life out " +\
        "of me!\"}}"),

        "cat Eleanor": _("\n{{wb:Eleanor:}} {{Bb:\"Where do you think the " +\
        "bell would have taken us?\"}}"),

        "cat dog": _("\n{{wb:Dog:}} {{Bb:\"Woof! Woof woof!\"}}")
    }
    hints = [
        _("{{gb:Edward looks like he has something he wants to say. " +\
        "Listen to Edward with}} {{yb:cat Edward}}")
    ]

    def check_command(self, line):
        line = line.strip()
        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            self.send_hint(hint)
            return
        return StepTemplateMv.check_command(self, line)

    def next(self):
        return 13, 1
