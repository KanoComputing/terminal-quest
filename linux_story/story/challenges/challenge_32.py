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
        "Clara said that he was in the woods just off the {{lb:Windy Road}} {{yb:~}}.",
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
        "{{lb:Go into the}} {{Bb:clearing}}"
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

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step8()


class Step8(StepTemplateNano):
    story = [
        "Huh, you can't seem to look inside.",
        "It is locked in the same way the {{bb:private-section}} in the library is.",
        "Maybe there's a clue somewhere around here.",
        "",
        "{{lb:Investigate}} the area and see if you can find any clues."
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
        Step9()


class Step9(StepTemplateNano):
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
        NextStep()



