#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

from ..Step import Step
from challenge_3 import Step1 as Step1_next


class Step1(Step):
    story = [
        "entered fork!"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = ""
    hint = "forky forky fork"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step1_next()
