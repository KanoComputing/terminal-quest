#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

# from linux_story.Step import Step
from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_5 import Step1 as NextChallengeStep
from linux_story.helper_functions import play_sound
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(TerminalCd):
    challenge_number = 4


class Step1(StepTemplateCd):
    story = [
        "That's weird. No time for that now though - lets find Mum.",
        "\n{{wb:New Spell}}: {{lb:cd}} lets you move between places.",
        "\nUse the command {{yb:cd ../}} to leave your room.\n"
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house"
    commands = [
        "cd ..",
        "cd ../",
        "cd ~/my-house",
        "cd ~/my-house/"
    ]
    hints = [
        "{{rb:Type}} {{yb:cd ../}} {{rb:to leave your room. The}} "
        "{{lb:..}} "
        "{{rb:is the room behind you.}}",
        "{{rb:Type}} {{yb:cd ../}} {{rb:to leave your room.}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "You've left {{lb:my-room}} and are in the hall of {{lb:my-house}}.",
        "Have a look at the different rooms around you using {{yb:ls}}\n"
    ]
    start_dir = "~/my-house"
    end_dir = "~/my-house"
    commands = "ls"
    hints = "{{rb:Type}} {{yb:ls}} {{rb:and press Enter.}}"
    story_dict = {
        "note_greenhouse": {
            "name": "note",
            "path": "~/my-house/garden/greenhouse"
        }
    }
    deleted_items = ['~/my-house/garden/greenhouse/Dad']

    def next(self):
        play_sound('bell')
        Step3()


class Step3(StepTemplateCd):
    story = [
        "{{pb:Ding. Dong.}}\n",
        "What was that?  A bell?  That's a bit odd.",
        "You see the door to your kitchen, and hear the sound of cooking.",
        "Sounds like someone is preparing breakfast!",
        "To go inside the kitchen, use {{yb:cd kitchen/}}"
    ]
    start_dir = "~/my-house"
    end_dir = "~/my-house/kitchen"
    commands = ["cd kitchen", "cd kitchen/"]
    hints = ["{{rb:Type}} {{yb:cd kitchen/}} {{rb:and press Enter.}}"]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Great, you're in the kitchen.",
        "Try and find Mum using {{yb:ls}}"
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = "ls"
    hints = "{{rb:Can't find her?  Type}} {{yb:ls}} {{rb:and press Enter.}}"

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "You see her busily working in a cloud of steam.",
        "Let's see what {{lb:Mum}} has to say by using {{lb:cat}}."
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = "cat Mum"
    hints = (
        "{{rb:Stuck? Type:}} {{yb:cat Mum}}. "
        "{{rb:Don\'t forget the capital letter!}}"
    )

    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
