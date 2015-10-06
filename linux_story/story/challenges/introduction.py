#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
from linux_story.Terminal import Terminal
from linux_story.story.challenges.challenge_1 import Step1 as NextChallengeStep


class StepTemplateLs(Terminal):
    challenge_number = 0


class Step1(StepTemplateLs):
    story = [
        "Ciao {}.".format("{{yb:" + os.environ['LOGNAME'] + "}}"),
        "Benvenuto nel lato oscuro di  Kano.",
        "Sei entrato in un mondo pericoloso dove le parole "
        "danno poteri speciali.",
        "Pronto?  Premi {{gb:Invio}} per iniziare."
    ]
    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"

    def next(self):
        NextChallengeStep()
