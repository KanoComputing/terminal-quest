#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
from linux_story.Step import Step
from linux_story.Terminal import Terminal
from linux_story.story.challenges.challenge_1 import Step1 as NextChallengeStep


class StepTemplateLs(Step):
    challenge_number = 0

    def __init__(self):
        Step.__init__(self, Terminal)


class Step1(StepTemplateLs):
    story = [
        "Hello {}.".format("{{yb:" + os.environ['LOGNAME'] + "}}"),
        "Welcome to the dark side of your Kano.",
        "You've entered a perilous world where words "
        "wield power.",
        "Ready?  Press {{gb:Enter}} to begin."
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    def next(self):
        NextChallengeStep()
