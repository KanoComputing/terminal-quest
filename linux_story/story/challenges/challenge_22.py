#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.Step import Step
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
# from linux_story.story.challenges.challenge_23 import Step1 as NextChallengeStep


class StepTemplateMkdir(Step):
    challenge_number = 22

    def __init__(self, xp=''):
        Step.__init__(self, TerminalMkdir, xp)


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:Nice work!}}",
        "\nRuth: {{Bb:Thank you so much! "
        "We'll stay in here to keep safe.  I'm so grateful to everything you've done}}",
        "{{Bb:Do you think there are others like me, who could "
        "be stranded and in hiding?}}",
        "\nMaybe you could check back on the family in the {{yb:.hidden-shelter}} ",
        "and see if you can talk with your new found voice.",
        "Head back to the {{yb:.hidden-shelter}}."
    ]

    start_dir = "~/farm/toolshed"
    end_dir = "~/town/.hidden-shelter"

    def block_command(self):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Have a look around"
    ]

    start_dir = "~/town/.hidden-shelter",
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls",
        "ls -a"
    ]

    def check_command(self, line, current_dir):
        pass
        # if "ls -a, try and skip ahead to Step 4"
