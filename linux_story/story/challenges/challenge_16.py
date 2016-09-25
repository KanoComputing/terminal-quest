# challenge_16.py
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

from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.challenges.challenge_17 import Step1 as NextStep
# import time


class StepTemplateMv(TerminalMv):
    challenge_number = 16


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        _("There is an old antique {{bb:.chest}} hidden under your bed, which you don't remember seeing before.\n"),
        _("You walk into {{bb:my-room}} to have a closer look.\n"),
        _("{{lb:Peer inside}} the {{bb:.chest}} and see what it contains.")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    commands = [
        'ls .chest',
        'ls .chest/',
        'ls -a .chest',
        'ls -a .chest/',
        'ls .chest/ -a',
        'ls .chest -a'
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls .chest}} {{rb:to look inside the .chest}}")
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        _("There are some rolls of parchment, similar to what you found in the {{bb:.hidden-shelter}}\n"),
        _("Use {{yb:cat}} to {{lb:read}} one of the scrolls.\n")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    commands = [
        'cat .chest/LS',
        'cat .chest/CAT',
        'cat .chest/CD'
    ]

    hints = [
        _("{{rb:Use}} {{yb:cat .chest/LS}} {{rb:to read the LS scroll.}}")
    ]

    def next(self):
        Step3()


# Remove this step?
'''
class Step3(StepTemplateMv):
    story = [
        _("You recognise these commands."),
        _("Maybe you should {{lb:move}} the one you found in the {{lb:~/town/.hidden-shelter/.tiny-chest}} to this {{lb:.chest}}, so they're all safe and in the same place."),
        _("\n{{gb:Use the}} {{ob:TAB}} {{gb:key to complete the file paths - it will save you typing!}}\n")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    commands = [
        "mv ~/town/.hidden-shelter/.tiny-chest/MV .chest/",
        "mv ~/town/.hidden-shelter/.tiny-chest/MV .chest",
        "mv ../../.hidden-shelter/.tiny-chest/MV .chest/",
        "mv ../../.hidden-shelter/.tiny-chest/MV .chest",
        "mv ~/town/.hidden-shelter/.tiny-chest/MV ~/my-house/my-room/.chest/",
        "mv ~/town/.hidden-shelter/.tiny-chest/MV ~/my-house/my-room/.chest"
    ]
    hints = [
        _("{{rb:You want to use the command}} {{yb:mv ~/town/.hidden-shelter/.tiny-chest/MV .chest/}}\n{{rb:Use the UP arrow to replay your last command if you were close!}}")
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step4()
'''


class Step3(StepTemplateMv):
    story = [
        _("I wonder if there's anything else hidden in this {{lb:.chest}}?"),
        _("Have a {{lb:closer look}} for some more items.")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    hints = [
        _("{{rb:Use}} {{yb:ls -a .chest}} {{rb:to see if there are any hidden items in the chest.}}")
    ]

    commands = [
        "ls -a .chest",
        "ls -a .chest/",
        'ls .chest/ -a',
        'ls .chest -a'
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        _("You suddenly notice a tiny stained {{lb:.note}}, scrumpled in the corner of the {{lb:.chest}}."),
        _("What does it say?\n")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    hints = [
        _("{{rb:Use}} {{yb:cat .chest/.note}} {{rb:to read the}} {{lb:.note}}{{rb:.}}")
    ]

    commands = [
        "cat .chest/.note"
    ]

    def next(self):
        NextStep(self.xp)
