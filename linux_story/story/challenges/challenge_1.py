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
from linux_story.story.terminals.terminal_ls import TerminalLs
from linux_story.story.challenges.challenge_2 import Step1 as NextChallengeStep


class StepTemplateLs(Step):
    def __init__(self):
        Step.__init__(self, TerminalLs)


class Step1(StepTemplateLs):
    story = [
        "{{wb:Alarm}} : \"Beep beep beep! Beep beep beep!\"",
        "{{wb:Radio}} : {{Bb:\"Good Morning, this is the 7am news.\"",
        "\"There have been reports of strange activity occurring in the town "
        "of Folderton today, as the number of reports of missing people and "
        "damaged buildings continues to increase...\"",
        "\"...nobody can explain what is causing the phenomenon, and Mayor "
        "Hubert has called an emergency town meeting...\"}}\n",
        "It's time to get up sleepy head!",
        "\n{{wb:New Spell:}} {{yb:ls}} - lets you see what's around you."
    ]
    start_dir = "my-room"
    end_dir = "my-room"
    command = "ls"
    hints = [
        "{{rb:Type}} {{yb:ls}} {{rb:and press Enter to take a look around "
        "your bedroom}}"
    ]

    challenge_number = 1
    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
