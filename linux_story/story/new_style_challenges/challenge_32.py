#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.new_terminals.terminal_nano import TerminalNano


class StepTemplateNano(StepTemplate):
    TerminalClass = TerminalNano


class Step1(StepTemplateNano):
    story = [
        _("Time to find the swordmaster."),
        _("Clara said that he was in the woods just off the {{lb:Windy Road}} {{yb:~}}."),
        _("Use {{yb:cd}} to head there now.")
    ]
    start_dir = "~/town/east/shed-shop/basement"
    end_dir = "~"
    hints = [
        _("{{rb:Use}} {{yb:cd}} {{rb:by itself to go back to the Windy Road ~}}")
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
        }
    ]

    # Maybe this could be reduced to an argument in the class.
    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 32, 2


class Step2(StepTemplateNano):
    story = [
        _("{{lb:Look around}} to see where the woods are.")
    ]
    start_dir = "~"
    end_dir = "~"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Look around using}} {{yb:ls}}")
    ]

    def next(self):
        return 32, 3


class Step3(StepTemplateNano):
    story = [
        _("You see the {{bb:woods}} in the distance, a set of dark and inhospitable trees."),
        _("{{lb:Go into the woods}}.")
    ]
    start_dir = "~"
    end_dir = "~/woods"
    hints = [
        _("{{rb:Use}} {{yb:cd woods/}} {{rb:to go to the woods.}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 32, 4


# Should they use ls -a to find something hidden?
class Step4(StepTemplateNano):
    story = [
        _("{{lb:Look around}} and see where to go next.")
    ]
    start_dir = "~/woods"
    end_dir = "~/woods"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Look around using}} {{yb:ls}}")
    ]

    def next(self):
        return 32, 5


class Step5(StepTemplateNano):
    story = [
        _("You see a {{bb:clearing}} which reminds you of a garden."),
        _("{{lb:Go into the}} {{bb:clearing}}{{lb:.}}")
    ]
    start_dir = "~/woods"
    end_dir = "~/woods/clearing"
    commands = [
        "cd clearing/",
        "cd clearing"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cd clearing/}} {{rb:to go into the clearing.}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 33, 1



