#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.common import get_story_file
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.challenges.challenge_33 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateNano(TerminalNano):
    challenge_number = 32


class Step1(StepTemplateNano):
    story = [
        "Time to find the swordmaster.",
        "Clara said that he was in the woods just off the {{lb:Windy Road}} {{yb:~}}.",
        "Use {{yb:cd}} to head there now."
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~"
    hints = [
        "{{rb:Remember, use}} {{yb:cd}} {{rb:by itself to go back to the "
        "Windy Road ~}}"
    ]

    file_list = [
        {
            "path": "~/woods/clearing/house",
            "permissions": 0000,
            "type": "directory"
        },
        {
            "path": "~/woods/clearing/signpost",
            "permissions": 0644,
            "type": "file",
            "contents": get_story_file("signpost")
        },
        {
            "path": "~/woods/clearing/weed",
            "permissions": 0644,
            "type": "file",
            "contents": get_story_file("weed")
        }
    ]

    # Maybe this could be reduced to an argument in the class.
    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Look around to see where the woods are."
    ]
    start_dir = "~"
    end_dir = "~"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Look around using}} {{yb:ls}}"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "You see a set of trees in the distance. They seem very dark and "
        "inhospitable, which is why you didn't notice them before.",
        "{{lb:Go into the woods}}."
    ]
    start_dir = "~"
    end_dir = "~/woods"
    hints = [
        "{{rb:Use}} {{yb:cd woods/}} {{rb:to go to the woods.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


# Should they use ls -a to find something hidden?
class Step4(StepTemplateNano):
    story = [
        "Look around and see where to go next."
    ]
    start_dir = "~/woods"
    end_dir = "~/woods"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Look around using}} {{yb:ls}}"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    story = [
        "You see a {{bb:clearing}} which reminds you of a garden.",
        "{{lb:Go into the}} {{bb:clearing}}"
    ]
    start_dir = "~/woods"
    end_dir = "~/woods/clearing"
    commands = [
        "cd clearing/",
        "cd clearing"
    ]
    hints = [
        "{{rb:Use}} {{yb:cd clearing/}} {{rb:to go into the clearing.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep()



