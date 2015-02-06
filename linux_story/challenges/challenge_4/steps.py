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
from terminals import TerminalCd
from linux_story.challenges.challenge_5.steps import Step1 as NextChallengeStep
from linux_story.helper_functions import play_sound


class StepTemplateCd(Step):
    challenge_number = 4

    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gb:Congratulations, you earned 7 XP!}}\n",
        "That's weird. No time for that now though - lets find Mum.",
        "\n{{wb:New Spell}}: {{yb:cd}} lets you move between places.",
        "\nTo leave your room, use the command {{yb:cd ..}}"
    ]
    start_dir = "my-room"
    end_dir = "my-house"
    command = ""
    hints = (
        "{{rb:Type}} {{yb:cd ..}} {{rb:to leave your room}}"
    )

    def block_command(self, line):
        allowed_commands = [
            "cd ..",
            "cd ../",
            "cd ~/my-house",
            "cd ~/my-house/"
        ]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "You are now in the main hall of your house",
        "Have a look at the different rooms of your house using {{yb:ls}}"
    ]
    start_dir = "my-house"
    end_dir = "my-house"
    command = "ls"
    hints = "{{r:Type}} {{yb:ls}} {{r:and press Enter.}}"

    def next(self):
        play_sound('bell')
        Step3()


class Step3(StepTemplateCd):
    story = [
        "What was that?  A bell?  That's a bit odd.",
        "You see the door to your kitchen, and hear the sound of cooking.",
        "Sounds like someone is preparing dinner!",
        "To go inside the kitchen, use {{yb:cd kitchen}}."
    ]
    start_dir = "my-house"
    end_dir = "kitchen"
    command = ""
    hints = ["{{rb:Type}} {{yb:cd kitchen}} {{rb:and press Enter.}}"]

    def block_command(self, line):
        allowed_commands = ["cd kitchen", "cd kitchen/"]
        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "You are in the kitchen.",
        "Try and find Mum using {{yb:ls}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "ls"
    hints = "{{rb:Can't find her?  Type}} {{yb:ls}} {{rb:and press Enter.}}"

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "You see your mum busily working in a cloud of steam",
        "Let's see what {{yb:mum}} wants by using {{yb:cat}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "cat mum"
    hints = "{{rb:Stuck? Type:}} {{yb:cat mum}}"

    last_step = True
    challenge_number = 4

    def next(self):
        NextChallengeStep()
