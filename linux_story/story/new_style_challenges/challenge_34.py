#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.helper_functions import wrap_in_box
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.new_terminals.terminal_chmod import TerminalChmod
from linux_story.story.new_terminals.terminal_nano import TerminalNano


class StepTemplateNano(StepTemplate):
    TerminalClass = TerminalNano


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateNano):
    story = [
        _("There are three rooms."),
        _("First, {{lb:look inside the dark-room}}.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls dark-room",
        "ls dark-room/"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls dark-room/}} {{rb:to look inside the dark-room.}}")
    ]

    def next(self):
        return 34, 2


class Step2(StepTemplateNano):
    story = [
        _("The room is pitch black, and it is impossible to see anything inside."),
        _("Next, {{lb:look inside}} the {{bb:locked-room}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls locked-room",
        "ls locked-room/"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls locked-room/}} {{rb:to look inside the locked-room.}}")
    ]

    def next(self):
        return 34, 3


class Step3(StepTemplateNano):
    story = [
        _("Peering through a grimy window, you can just make out the items inside."),
        _("{{lb:Examine the items inside}}.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat locked-room/sign",
        "cat locked-room/firework"
    ]
    hints = [
        _("{{rb:Examine the sign with}} {{yb:cat locked-room/sign}}")
    ]

    def next(self):
        return 34, 4


class Step4(StepTemplateNano):
    story = [
        _("You are unable to make out the items in the room."),
        _("Maybe it would help if you went inside?"),
        _("Try and {{lb:go inside}} the {{bb:locked-room}}.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    dirs_to_attempt = "~/woods/cave/locked-room"
    hints = [
        _("{{rb:Go inside the locked-room with}} {{yb:cd locked-room}}")
    ]
    commands = [
        "cd locked-room",
        "cd locked-room/"
    ]

    def block_command(self, last_user_input):
        return unblock_commands(last_user_input, self.commands)

    def next(self):
        return 34, 5


class Step5(StepTemplateNano):
    story = [
        _("The door is locked, so you can't go in."),
        _("Finally, {{lb:look inside}} the {{bb:cage}}.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls cage",
        "ls cage/"
    ]
    hints = [
        _("{{rb:Look inside the cage with}} {{yb:ls cage}}")
    ]

    def next(self):
        return 34, 6


class Step6(StepTemplateNano):
    story = [
        _("There is a bird in the cage. {{lb:Examine}} the bird."),
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat cage/bird"
    ]
    hints = [
        _("{{rb:Examine the bird with}} {{yb:cat cage/bird}}")
    ]

    def next(self):
        return 34, 7


class Step7(StepTemplateNano):
    story = [
        _("Bird: {{Bb:...Me...trapped..}}"),
        _("{{Bb:Please help....get me out.}}"),
        "",
        _("Help the bird by {{lb:moving}} the {{lb:bird}} outside the {{lb:cage}}.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "mv cage/bird .",
        "mv cage/bird ./"
    ]
    hints = [
        _("{{rb:Move the bird outside the cage with}} {{yb:mv cage/bird ./}}")
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 34, 8



class Step8(StepTemplateChmod):
    story = [
        "You are unable to move the bird outside the cage.",
        "Bird: {{Bb:...didn't work....}}",
        "{{Bb:...look in}} {{lb:dark-room}} {{Bb:to find help..}}",
        "{{Bb:..use}} {{yb:chmod +r dark-room}} {{Bb:to switch lights on.}}",
        "{{Bb:...get me out...and I'll help you.}}",
        ""
    ]
    story += wrap_in_box([
        _("{{gb:New Spell:}} Use "),
        _("{{yb:chmod +r dark-room}} "),
        _("to allow yourself to {{lb:read}} "),
        _("the contents of dark-room.")
    ])

    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "chmod +r dark-room",
        "chmod +r dark-room/"
    ]
    highlighted_commands = "chmod"
    hints = [
        "{{rb:Follow the bird's instructions and use}} {{yb:chmod +r dark-room}} {{rb:to turn the lights on in the}} "
        "{{bb:dark-room.}}"
    ]

    def next(self):
        return 35, 1
