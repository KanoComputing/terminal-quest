#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
# from linux_story.story.challenges.challenge_29 import Step1 as NextChallengeStep


class StepTemplateNano(TerminalNano):
    challenge_number = 28


class Step1(StepTemplateNano):
    story = [
        "Where could the librarian be hiding?",
        "{{lb:Look around}} to decide where to go next."
    ]

    start_dir = "~/town/east-part"
    end_dir = "~/town/east-part"

    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    commands = [
        "ls",
        "ls -a"
    ]

    def next(self):
        pass
