#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os

from linux_story.common import get_username
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.challenges.challenge_34_talk_to_swordmaster import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateNano(TerminalNano):
    challenge_number = 33


class Step1(StepTemplateNano):
    story = [
        "You hear a deep voice on the other side of the door.",
        "",
        "Swordmaster: {{Bb:Hello? Who's there?}}",
        "",
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
        "swordmaster": {
            "name": "swordmaster",
            "path": "~/woods/clearing/house"
        },
        "basement": {
            "directory": True,
            "path": "~/woods/clearing/house",
            "permissions": 0000
        },
        # Directory with the read permissions removed
        "dark-room": {
            "directory": True,
            "permissions": 0300,
            "path": "~/woods/clearing/house/dark-room"
        },
        "bookshelf": {
            "path": "~/woods/clearing/house/dark-room"
        },
        "desk_swordsmaster": {
            "name": "desk",
            "path": "~/woods/clearing/house/dark-room"
        },
        "READ-ME": {
            "path": "~/woods/clearing/house/dark-room",
            "permissions": 0200
        },
        "cage-room": {
            "directory": True,
            "path": "~/woods/clearing/house",
        },
        "bird": {
            "path": "~/woods/clearing/house/cage-room",
            "permissions": 0644
        },
        "no-entry-room": {
            "directory": True,
            "path": "~/woods/clearing/house",
        },
        "RUN-ME": {
            "path": "~/woods/clearing/house/no-entry-room",
            "permissions": 0600
        }
    }

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

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
    story_dict = {
        "cage-room": {
            "directory": True,
            "path": "~/woods/clearing/house",
            "permissions": 0500
        },
        "no-entry-room": {
            "directory": True,
            "path": "~/woods/clearing/house",
            "permissions": 0600
        }
    }
    commands = [
        "ls",
        "ls -a"
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
