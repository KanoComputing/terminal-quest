#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.challenges.challenge_33 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateNano(TerminalNano):
    challenge_number = 32


class Step1(StepTemplateNano):
    story = [
        "Time to find the swordmaster.",
        "Ruth said that he was in the woods just off the "
        "{{lb:Windy Road}} {{yb:~}}.",
        "Use {{yb:cd}} to head there now."
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~"
    # Need to deactivate the cd hints.
    hints = [
        "{{rb:Remember, use}} {{yb:cd}} {{rb:by itself to go back to the "
        "Windy Road ~}}"
    ]

    story_dict = {
        "house": {
            "directory": True,
            "path": "~/woods/clearing",
            "permissions": 0000
        },
        "signpost": {
            "path": "~/woods/clearing"
        },
        "weed": {
            "path": "~/woods/clearing"
        },
        "doorbell.sh": {
            "path": "~/woods/clearing",
            "permissions": 0755
        },
        "thicket": {
            "directory": True,
            "path": "~/woods"
        }
    }

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

    # Perhaps a nice data structure could be if the list of commands were
    # paired with appropriate hints?
    # E.g. if we need the user to do "ls -a" and they do "ls", could give a
    # different set of hints

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    story = [
        "You see a {{bb:clearing}} which reminds you of a garden.",
        "Try and {{lb:go into the clearing.}}"
    ]
    start_dir = "~/woods"
    end_dir = "~/woods/clearing"
    commands = [
        "cd clearing/"
    ]
    hints = [
        "{{rb:Use}} {{yb:cd clearing/}} {{rb:to go into the clearing.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step6()


class Step6(StepTemplateNano):
    story = [
        "Look around the clearing.",
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Look around the clearing with}} {{yb:ls}}"
    ]

    def next(self):
        Step7()


class Step7(StepTemplateNano):
    story = [
        "There's a house in the clearing. Have a {{lb:look}} in the {{lb:house}}, or try and {{lb:go inside}}.",
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    dirs_to_attempt = "~/woods/clearing/house"
    commands = [
        "ls house",
        "ls house/",
        "ls -a house",
        "ls -a house/",
        "cd house",
        "cd house/"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls house/}} {{rb:to look in the house.}}"
    ]
    last_step = True

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)
