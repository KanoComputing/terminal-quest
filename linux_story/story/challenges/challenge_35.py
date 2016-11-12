#!/usr/bin/env python
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.step_helper_functions import unblock_commands_with_cd_hint, unblock_cd_commands
from linux_story.story.challenges.challenge_36 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 35


class Step1(StepTemplateNano):
    story = [
        "Swordsmaster: {{Bb:Your name is written in this world, for anyone who knows where to look. Use}} {{yb:ls -l}} "
        "{{Bb:to see.}}"
    ]
    commands = [
        "ls -l"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    def next(self):
        Step2()


class Step2(StepTemplateNano):

    story = [
        "Swordsmaster: {{Bb:See your name on everything in this house? You have extra permissions in this world, "
        "and the best chance of stopping people disappearing.}}",
        "{{Bb:I will teach you how to unlock the private section.}}",
        "{{Bb:First,}} {{lb:go into the basement}} {{Bb:in this room.}}"
    ]
    commands = [
        "ls",
        "ls .",
        "ls ./",
        "ls -a",
        "ls -a .",
        "ls -a ./",
        "cd basement",
        "cd basement/"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    dirs_to_attempt = "~/woods/clearing/house/basement"

    def __init__(self):
        self.__counter = 0
        StepTemplateNano.__init__(self)

    def check_command(self):
        self.__counter += 1
        if self.__counter >= 2:
            if self.last_user_input.strip().startswith("ls") and self.last_user_input in self.commands:
                self.send_hint("\nSwordsmaster: {{Bb:Good! Now use}} {{yb:cd basement/}}")
            else:
                self.send_hint("\nSwordsmaster: {{Bb:Why the delay? Use}} {{yb:cd basement/}} {{Bb:to go inside.}}")
            return
        else:
            return StepTemplateNano.check_command(self)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Swordsmaster: {{Bb:Go into the basement you see.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = ["cd basement"]

    def check_command(self):
        if self.last_user_input.strip() in self.commands:
            print "-bash: cd: basement: Permission denied"
            return True
        else:
            self.send_hint("{{rb:Use}} {{yb:cd basement/}} {{rb:to go into the basement.}}")
            return False

    def block_command(self):
        if self.last_user_input.startswith("cd"):
            return True

    def next(self):
        Step4()


# Make directory executable
class Step4(StepTemplateNano):
    story = [
        "Swordsmaster: {{Bb:You got the error}} {{yb:-bash: cd: basement: Permission denied}}",
        "{{Bb:Normally you can do 3 things to a directory.}}",
        "",
        "{{Bb:See what is inside -}} {{lb:read}}",
        "{{Bb:Create something inside -}} {{lb:write}}",
        "{{Bb:Go inside with cd -}} {{lb:execute}}",
        "",
        "{{Bb:This directory is missing all three.}}"
        "",
        "{{Bb:To go inside, you need to activate the execute one.}}",
        "{{Bb:Use}} {{yb:chmod +x basement}} {{Bb:to unlock the basement.}}"
    ]
    commands = [
        "chmod +x basement",
        "chmod +x basement/"
    ]
    hints = [
        "{{rb:Use}} {{yb:chmod +x basement/}} {{rb:to unlock the basement.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    last_step = True

    def next(self):
        NextStep()
