#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        _("The bird dropped a {{bb:scroll}} in the {{bb:cage}}."),
        _("{{lb:Examine}} the scroll.")
    ]

    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat cage/scroll"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat cage/scroll}} {{rb:to examine the scroll.}}")
    ]
    file_list = [
        {
            "path": "~/woods/cave/cage/scroll",
            "contents": get_story_file("scroll-cage")
        }
    ]
    deleted_items = [
        "~/woods/cave/bird"
    ]

    def next(self):
        return 36, 2


class Step2(StepTemplateChmod):
    story = [
        _("Follow the instructions. Use {{yb:chmod +x}} on the {{bb:lighter}} in the {{bb:locked-room}}.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "chmod +x locked-room/lighter"
    ]
    hints = [
        _("{{rb:Use}} {{yb:chmod +x locked-room/lighter}} {{rb:to activate the lighter.}}")
    ]
    highlighted_commands = "chmod"

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 36, 3


class Step3(StepTemplateChmod):
    story = [
        _("{{lb:Look in the locked-room}} to see what happened to the lighter.")
    ]

    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"

    commands = [
        "ls locked-room",
        "ls locked-room/"
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls locked-room/}} {{rb:to look in the locked-room.}}")
    ]

    def next(self):
        return 36, 4


class Step4(StepTemplateChmod):
    story = [
        _("The lighter went {{gb:bright green}} after you activated it."),
        _("Now use it with {{yb:./locked-room/lighter}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"

    commands = [
        "./locked-room/lighter"
    ]

    def next(self):
        return 37, 1
