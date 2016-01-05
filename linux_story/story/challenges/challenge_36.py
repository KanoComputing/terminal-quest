#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import (
    unblock_cd_commands, unblock_commands
)
from linux_story.story.challenges.challenge_37 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 36


# Instead of a sandwich, make this a script, and then the last task is to make
# it executable.
class Step1(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Well done. You've made the basement readable, "
        "and you can see there is a}} {{lb:key.sh}} {{Bb:in there.}}",
        "{{lb:Read the contents of key.sh.}}"
    ]
    commands = [
        "cat key.sh"
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    hints = [
        "{{rb:Use}} {{yb:cat key.sh}} {{rb:to read the contents of "
        "key.sh}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:The key.sh has also had its permissions removed.}}",
        "{{yb:Can you remember how to make it readable?}}"
    ]
    commands = [
        "chmod +r key.sh"
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    hints = [
        "{{rb:Use}} {{yb:chmod +r key.sh}} {{rb:to make key.sh readable.}}"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Now try and read key.sh again.}}"
    ]
    commands = [
        "cat key.sh"
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    hints = [
        "{{rb:Use}} {{yb:cat key.sh}} {{rb:to read the contents of key.sh}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:This key.sh acts on the basement. ",
        "By using -  instead of +, it removes the permissions from basement.",
        "For it to work, it should be moved outside the basement to where I am.}}",
        "",
        "{{Bb:Move the}} {{lb:key.sh}} {{Bb:back to ../}}"
    ]
    commands = [
        "mv key.sh ../",
        "mv key.sh .."
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    hints = [
        "{{rb:Use}} {{yb:mv key.sh ../}} {{rb:to move the key outside the basement.}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Now you get the error}} {{yb:mv: cannot move "
        "key.sh to ../key.sh: Permission denied}}",
        "",
        "{{Bb:This is the final permission you need to enable - the write "
        "permission.",
        "This permission allows you to change what is inside}} "
        "{{bb:basement}}{{Bb:.}}",
        "",
        "{{Bb:To give yourself this, use}} {{yb:chmod +w ./}}"
    ]
    commands = [
        "chmod +w ./",
        "chmod +w ."
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    hints = [
        "{{rb:Use}} {{yb:chmod +w ./}} {{rb:to make the current directory "
        "Writeable}}"
    ]

    def next(self):
        NextStep()
