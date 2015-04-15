#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.Step import Step
from linux_story.step_helper_functions import unblock_command_list
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
# from linux_story.story.challenges.challenge_23 import Step1 as NextChallengeStep


class StepTemplateMkdir(Step):
    challenge_number = 22

    def __init__(self, xp=''):
        Step.__init__(self, TerminalMkdir, xp)


class Step6(StepTemplateMkdir):
    story = [
        "{{gb:Nice work!}}",
        "\nRuth: {{Bb:Thank you so much! "
        "We'll stay in here to keep safe.  I'm so grateful to everything you've done}}",
        "{{Bb:Do you think there are others like me, who could "
        "be stranded and in hiding?}}"
    ]
