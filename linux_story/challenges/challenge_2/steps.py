#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.Step import Step
from terminals import TerminalCat
from linux_story.challenges.challenge_3.steps import Step1 as NextChallengeStep
from linux_story.file_functions import write_to_file


class StepTemplateCat(Step):
    def __init__(self):
        Step.__init__(self, TerminalCat)


class Step1(StepTemplateCat):
    story = [
        "{{gCongratulations, you earned 5 XP!}}\n",
        "Better turn that alarm off.",
        "\n{{wNew Spell}}: to look at objects, we type {{ycat <object name>}}.",
        "To look at the alarm, type {{ycat alarm}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat alarm"
    hints = "{{rType}} {{ycat alarm}} {{rto see the alarm.}}"

    def next(self):
        Step2()


class Step2(StepTemplateCat):
    story = [
        "Ok - it's switched off. Better get dressed...",
        "Type {{yls wardrobe}} to find something to wear"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls wardrobe", "ls wardrobe/"]
    hints = "{{rType {{yls wardrobe}} to find something to wear}}"

    def next(self):
        Step3()


class Step3(StepTemplateCat):
    story = [
        "Type {{ycat wardrobe/hat}} to see how it looks"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat wardrobe/hat"
    hints = "{{rType}} {{ycat wardrobe/hat}} {{rto find something to wear}}"

    def next(self):
        write_to_file("challenge", "3")
        NextChallengeStep()
