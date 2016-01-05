#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
from linux_story.story.challenges.challenge_35 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 34


class StepTemplateChmod(TerminalChmod):
    challenge_number = 34


class Step1(StepTemplateNano):
    story = [
        "You see a masked swordsmaster watching you.",
        "Listen to what he has to say."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:cat swordsmaster}} {{rb:to}} {{lb:listen}} "
        "{{rb:to what the swordsmaster has to say.}}"
    ]
    commands = [
        "cat swordsmaster"
    ]

    def next(self):
        Step2()


# TODO: fill in the extra responses to the other questions
class Step2(StepTemplateNano):
    story = [
        "{{wb:Swordsmaster:}} {{Bb:Child, why do you seek me?}}",
        "",
        "{{yb:1: How did you lock your front door?}}",
        "{{yb:2: Who are you?}}",
        "{{yb:3: Have you been leaving me the strange notes?}}",
        "",
        "Respond with {{yb:echo 1}}, {{yb:echo 2}}, or {{yb:echo 3}}."
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} "
        "{{yb:echo 3}}{{rb:.}}"
    ]
    extra_hints = {
        "echo 2": "Swordsmaster: {{Bb:That is none of your business.}}",
        "echo 3": "Swordsmaster: {{Bb:What notes?}}"
    }

    def check_command(self):

        if self.last_user_input in self.extra_hints:
            hint = self.extra_hints[self.last_user_input]
            self.send_hint(hint)

        return StepTemplateNano.check_command(self)

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    print_text = [
        "{{yb:How did you lock your front door?}}"
    ]
    story = [
        "Swordsmaster: {{Bb:I used a special command. Only those who have "
        "proved themselves may learn it.",
        # How does he know your name? Initially thought of ls -l.
        "I know of your name...it is written all over this world for those "
        "who know where to look.",
        # ...but are you who you say you are? (Give user a test?)
        "...Ok. I will teach how I lock my door and protect myself.",
        "First, try and}} {{lb:go inside my basement.}}"
    ]
    # This logic for commands doesn't work
    commands = [
        "cd basement",
        "cd basement/"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:cd basement/}} {{rb:to look in the basement.}}"
    ]
    needs_sudo = True

    def check_command(self):
        if self.last_user_input.strip() in self.commands:
            print "-bash: cd: basement: Permission denied"
            return True
        else:
            self.send_hint("{{rb:Use}} {{yb:cd basement/}} {{rb:to look in the basement.}}")
            return False

    def block_command(self):
        if self.last_user_input.startswith("cd"):
            return True

    def next(self):
        Step4()


# Make directory executable
class Step4(StepTemplateChmod):
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

    def next(self):
        NextStep()
