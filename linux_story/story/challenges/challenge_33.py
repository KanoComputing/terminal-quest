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
        "Huh, you can't seem to look inside.",
        "It seems to be locked in the same way that library door was.",
        "Maybe there's a clue somewhere around here.",
        "{{lb:Investigate}} the area around and see if you can find any clues."
    ]
    start_dir = "~/woods/clearing"

    # This should be an array of allowed directories you can end up in.
    # Perhaps an empty array means it doesn't matter where you end up.
    end_dir = "~/woods/clearing"

    hints = [
        "{{rb:Examine that signpost with}} {{yb:cat signpost}}{{rb:.}}"
    ]

    commands = [
        "cat signpost"
    ]

    # Perhaps a nice data structure could be if the list of commands were
    # paired with appropriate hints?
    paired_hints = {
        "ls": "Try examining the individual items with {{lb:cat}}."
    }

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "So the signpost has an instruction on it? Let's carry it out."
    ]

    # It would be good if we could pass the current dir across and this would
    # simply be the default?
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    hints = [
        "{{rb:Use}} {{yb:echo knock knock}} {{rb:to knock on the door.}}"
    ]

    commands = [
        "echo knock knock"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "You hear a deep voice on the other side of the door.",
        "",
        "Swordsmaster: {{Bb:Hello? Who's there?}}",
        "Tell him your name using {{lb:echo}}"
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo " + get_username()
    ]
    hints = [
        "{{rb:Use}} {{yb:echo " + get_username() + "}} {{rb:to give him your name}}"
    ]

    def next(self):
        path = self.generate_real_path("~/woods/clearing/house")
        os.chmod(path, 0755)
        Step4()


class Step4(StepTemplateNano):
    story = [
        "{{wb:Cluck.}} {{gb:It sounds like the door unlocked.}}",
        "",
        "{{lb:Go inside the house.}}"
    ]

    # Change permissions of the house directory here.
    start_dir = "~/woods/clearing"

    # This should be an array of allowed directories you can end up in.
    # Perhaps an empty array means it doesn't matter where you end up.
    end_dir = "~/woods/clearing/house"

    # Level up based on the output of the command.

    hints = [
        "{{rb:Use}} {{yb:cd house/}} {{rb:to go into the house.}}"
    ]

    story_dict = {
        "swordsmaster": {
            "path": "~/woods/clearing/house"
        },
        "basement": {
            "directory": True,
            "path": "~/woods/clearing/house",
            "permissions": 0000
        }
    }

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    # Perhaps a nice data structure could be if the list of commands were
    # paired with appropriate hints?

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
