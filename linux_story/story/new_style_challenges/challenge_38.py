#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

# Redo chapter 5 with the swordmaster.

import os

from linux_story.StepTemplate import StepTemplate
from linux_story.PlayerLocation import generate_real_path
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.new_terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        _("{{gb:You've found the answer to the swordmaster's riddle!}}"),
        "",
        _("{{lb:Go back to the swordmaster's clearing.}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/clearing"
    hints = [
        _("Head back to the {{lb:~/woods/clearing}} where the swordmaster lives."),
        _("{{rb:Use}} {{yb:cd ~/woods/clearing}} {{rb:to go back to the swordmaster's clearing.}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 38, 2


class Step2(StepTemplateChmod):
    story = [
        _("Knock on the swordmaster's door.")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo knock knock"
    ]
    hints = [
        _("{{rb:Use}} {{yb:echo knock knock}} {{rb:to knock on the swordmaster's door.}}")
    ]

    def next(self):
        return 38, 3


class Step3(StepTemplateChmod):
    story = [
        _("Swordmaster:"),
        _("{{Bb:If you have me, you want to share me."),
        _("If you share me, you haven't got me."),
        _("What am I?}}"),
        "",
        _("{{yb:1. A secret}}"),
        _("{{yb:2. I don't know}}"),
        "",
        _("Use {{lb:echo}} to reply.")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo 1",
        "echo secret",
        "echo a secret",
        "echo A secret",
        "echo \"secret\"",
        "echo \"a secret\"",
        "echo \"A secret\""
    ]

    def check_command(self, line):
        if line.startswith("echo ") and line not in self.commands:
            self.send_hint("Swordmaster: {{Bb:Incorrect. Did you finish the challenges in the cave? "
                           "The answer was in there.}}")
        return StepTemplateChmod.check_command(self, line)

    def next(self):
        path = generate_real_path("~/woods/clearing/house")
        os.chmod(path, 0755)
        return 38, 4


class Step4(StepTemplateChmod):
    story = [
        _("{{wb:Clunck.}} {{gb:It sounds like the door unlocked.}}"),
        "",
        _("{{lb:Go in the house.}}")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing/house"
    hints = [
        _("{{rb:Use}} {{yb:cd house}} {{rb:to go inside}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 38, 5


class Step5(StepTemplateChmod):
    story = [
        _("{{lb:Look around.}}")
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to go inside}}")
    ]
    commands = [
        "ls"
    ]

    def next(self):
        return 39, 1
