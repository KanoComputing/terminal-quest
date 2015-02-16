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


class StepTemplateCat(Step):
    challenge_number = 2

    def __init__(self):
        Step.__init__(self, TerminalCat)


class Step1(StepTemplateCat):
    story = [
        "{{gb:Congratulations, you earned 5 XP!}}\n",
        "Better turn that alarm off.",
        "\n{{wb:New Spell}}: to look at objects, we type {{yb:cat <object name>}}",
        "To look at the alarm, type {{yb:cat alarm}}"
    ]
    start_dir = "my-room"
    end_dir = "my-room"
    command = "cat alarm"
    hints = "{{rb:Type}} {{yb:cat alarm}} {{rb:to investigate the alarm.}}"

    def next(self):
        Step2()


class Step2(StepTemplateCat):
    story = [
        "Ok - it's switched off. Better get dressed...",
        "Type {{yb:ls wardrobe}} to find something to wear"
    ]
    start_dir = "my-room"
    end_dir = "my-room"
    command = ["ls wardrobe", "ls wardrobe/"]
    hints = "{{rb:Type}} {{yb:ls wardrobe}} {{rb:to find something to wear}}"

    def next(self):
        Step3()


class Step3(StepTemplateCat):
    story = [
        "Check out the {{yb:t-shirt}}",
        "Type {{yb:cat wardrobe/t-shirt}} to see how it looks"
    ]
    start_dir = "my-room"
    end_dir = "my-room"
    command = "cat wardrobe/t-shirt"
    hints = (
        "{{rb:Type}} {{yb:cat wardrobe/t-shirt}} "
        "{{rb:to investigate how it looks}}"
    )

    def next(self):
        Step4()


class Step4(StepTemplateCat):
    story = [
        "Looking good!  Put that on and look for something else",
        "Try on the {{yb:skirt}} or the {{yb:trousers}}"
    ]
    start_dir = "my-room"
    end_dir = "my-room"
    command = [
        "cat wardrobe/skirt",
        "cat wardrobe/trousers"
    ]
    hints = (
        "{{rb:Type}} {{yb:cat wardrobe/trousers}} {{rb:or}} "
        "{{yb:cat wardrobe/skirt}} {{rb:to dress yourself}}"
    )

    def next(self):
        Step5()


class Step5(StepTemplateCat):
    story = [
        "Awesome, you're nearly done.",
        "Finally, put on the {{yb:cap}} to finish off your outfit"
    ]
    start_dir = "my-room"
    end_dir = "my-room"
    command = [
        "cat wardrobe/cap"
    ]
    hints = (
        "{{rb:Type}} {{yb:cat wardrobe/cap}} {{rb:to finish "
        "off your outfit}}"
    )

    last_step = True

    def next(self):
        NextChallengeStep()
