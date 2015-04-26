#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.Step import Step
from linux_story.step_helper_functions import (
    unblock_commands
)
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
import time


class StepTemplateMkdir(Step):
    challenge_number = 23

    def __init__(self, xp=''):
        Step.__init__(self, TerminalMkdir, xp)


class Step1(StepTemplateMkdir):
    story = [
        "There's no one here anymore....where did they all go?",
        "That bell you heard earlier...could it have found this family?",
        "You remember it only rang twice...",
        "Have a closer look around."
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"

    hints = [
        "{{rb:Use}} {{yb:ls -a}} {{rb:to have a closer look around.}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Do you see those footprints?  They seem to be leading to "
        "{{yb:.tiny-chest}} in the corner.",
        "Have a look in the {{yb:.tiny-chest}}"
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls .tiny-chest",
        "ls -a .tiny-chest",
        "ls -a .tiny-chest/",
        "ls .tiny-chest/"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        "You see Eleanor curled up tightly inside the .tiny-chest.",
        "Help her {{yb:move}} outside the .tiny-chest back into the ",
        ".hidden-shelter"
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "mv .tiny-chest/Eleanor .",
        "mv .tiny-chest/Eleanor ./"
    ]
    hints = [
        "{{rb:Move Eleanor from the}} {{yb:.tiny-chest}} {{rb:to "
        "your current position using:}} {{yb:\nmv .tiny-chest/Eleanor .}}"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Check on Eleanor using {{yb:cat}}"
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "cat Eleanor"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat Eleanor}} {{to check on Eleanor}}"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Eleanor: {{Bb:Oh, it's you! Thank you for finding me!",
        "I heard this bell, and was so scared I squeezed in the "
        ".tiny-chest to hide.  Do you know where my Mum and Dad are?}}",
        "\n{{gb:Press Enter to continue.}}"
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    last_step = True

    def next(self):
        self.exit()

        # So that server has time to send message before it closes
        time.sleep(3)
