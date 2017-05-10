#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.Animation import Animation
from linux_story.StepTemplate import StepTemplate
from linux_story.helper_functions import wrap_in_box
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        _("{{lb:Look inside}} the dark room again.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls dark-room",
        "ls ./dark-room",
        "ls ./dark-room/",
        "ls dark-room/",
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls dark-room}} {{rb:to look inside the dark-room.}}")
    ]

    def next(self):
        return 35, 2


class Step2(StepTemplateChmod):
    story = [
        _("You can see a sign in the {{bb:dark-room}}. {{lb:Read the sign.}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat dark-room/sign"
    ]

    hints = [
        _("{{rb:Use}} {{yb:cat dark-room/sign}} {{rb:to read the sign.}}")
    ]

    def next(self):
        return 35, 3


class Step3(StepTemplateChmod):
    story = wrap_in_box([
        _("{{gb:New Power:}} Use"),
        _("{{yb:chmod +x locked-room}}"),
        _("to unlock the locked-room.")
    ])
    story += [
        _("Use it on the {{bb:locked-room}}.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    hints = [
        _("{{rb:Unlock the locked-room with}} {{yb:chmod +x locked-room}}")
    ]
    commands = [
        "chmod +x locked-room",
        "chmod +x locked-room/"
    ]
    highlighted_commands = "chmod"

    def next(self):
        return 35, 4


class Step4(StepTemplateChmod):
    story = [
        _("Now you can {{lb:examine}} the items in the {{bb:locked-room}}."),
        _("{{lb:Read the sign in the locked-room}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat locked-room/sign"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat locked-room/sign}} {{rb:to read the sign.}}")
    ]

    def check_commmand(self, line):
        if line == "cat locked-room/firework":
            self.send_hint("You see a firework.")
            return

        return StepTemplateChmod.check_command(self, line)

    def next(self):
        return 35, 5


class Step5(StepTemplateChmod):
    story = wrap_in_box([
        _("{{gb:New Spell:}} Type"),
        _("{{yb:chmod +w cage}}"),
        _("to give write permissions to,"),
        _("and thus unlock, the cage."),
    ])
    story += [
        "Try it out!"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "chmod +w cage",
        "chmod +w cage/"
    ]
    hints = [
        _("{{rb:Use}} {{yb:chmod +w cage}} {{rb:to unlock the cage.}}")
    ]

    def next(self):
        return 35, 6


class Step6(StepTemplateChmod):
    story = [
        _("Now you can help the bird escape from the cage."),
        _("{{lb:Move the bird outside the cage to where you are.}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "mv cage/bird .",
        "mv cage/bird ./"
    ]
    hints = [
        _("{{rb:Use}} {{yb:mv cage/bird ./}} {{rb:to move the bird outside.}}")
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        Animation("bird-animation").play_across_screen(speed=5)
        return 36, 1

