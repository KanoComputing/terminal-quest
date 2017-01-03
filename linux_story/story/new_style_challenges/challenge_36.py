#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.Animation import Animation
from linux_story.StepTemplate import StepTemplate
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.new_terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        _("Bird: {{Bb:...thank you.}}"),
        _("{{Bb:Do you like fireworks? There's one in the locked-room."),
        _("To blow it up, activate the lighter using}} {{yb:chmod +x}}")
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

    def _run_after_text(self):
        Animation("bird-animation").play_across_screen(speed=10)

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 36, 2


class Step2(StepTemplateChmod):
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
        return 36, 3


class Step3(StepTemplateChmod):
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
