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

from linux_story.story.terminals.terminal_ls import TerminalLs
from linux_story.story.challenges.challenge_2 import Step1 as NextChallengeStep


class StepLs(TerminalLs):
    challenge_number = 1


class Step1(StepLs):
    story = [
        "{{wb:Alarm}}: {{Bb:\"Beep beep beep! Beep beep beep!\"}}",
        "{{wb:Radio}}: {{Bb:\"Good Morning, this is the 9am news.\"",
        "\"The town of Folderton has awoken to strange news. "
        "\"There have been reports of missing people and damaged"
        " buildings across the town,"
        " with more stories coming in as we speak.\"",
        "Mayor Hubert has called an emergency town meeting and"
        " we'll keep you posted as it happens...\"}}\n",
        "It's time to get up sleepy head!\n ",
        "+----------------------------------------------------+",
        "| {{gb:New Spell:}} Type {{yb:ls}} and press {{wb:Enter}} to {{lb:look around}}. | " \
        "+----------------------------------------------------+\n"
    ]# TODO: " \ is a hack in this array to stop word wrap code screwing up and adding new lines in where it shouldn't
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "ls"
    hints = [
        "{{rb:Type}} {{yb:ls}} {{rb:and press {{ob:Enter}} to take a look around "
        "your bedroom.}}"
    ]

    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
