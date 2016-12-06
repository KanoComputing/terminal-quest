#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os

from linux_story.common import get_username
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.challenges.challenge_34 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateNano(TerminalNano):
    challenge_number = 33


class Step1(StepTemplateNano):
    story = [
        "We "
    ]