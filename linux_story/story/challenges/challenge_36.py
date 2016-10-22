#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import (
    unblock_cd_commands, unblock_commands,
    unblock_commands_with_cd_hint)
from linux_story.story.challenges.challenge_37 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 36


class Step1(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Well done. Now go inside the basement.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house/basement"
    commands = [
        "cd basement",
        "cd basement/"
    ]
    hints = [
        "{{rb:Use}} {{yb:cd basement/}} {{rb:to go inside the basement.}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(self.last_user_input,
                                             self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Look around.}}"
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"
    commands = [
        "ls", "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:You got the error}} {{yb:ls: cannot open directory .: Permission denied}}",
        "",
        "{{Bb:This is because you do not have permission to}} {{lb:read}} "
        "{{Bb:the contents of}} {{bb:basement}}{{Bb:.}}",
        "",
        "{{Bb:Use the command}} {{yb:chmod +r ./}} {{Bb:to be able to look "
        "around your current location.}}"
    ]
    commands = [
        "chmod +r .",
        "chmod +r ./"
    ]
    hints = [
        "{{rb:Use}} {{yb:chmod +r ./}} {{rb:to change the permissions on the basement.}}"
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:See if it worked.}} {{lb:Look around}}{{Bb:.}}"
    ]
    commands = [
        "ls",
        "ls -a",
        "ls ./",
        "ls ."
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    hints = [
        "{{rb:Look around using}} {{yb:ls}}{{rb:.}}"
    ]

    def next(self):
        NextStep(self.xp)
