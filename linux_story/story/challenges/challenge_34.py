#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.common import get_username
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
        "You see a Masked Swordsmaster watching you.",
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
        "{{yb:1: I want to unlock the private section in the library.}}",
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
        "echo 2": "Swordsmaster: {{Bb:I am one who has removed themselves from society. The few who know of me call me the Masked Swordsmaster.}}",
        "echo 3": "Swordsmaster: {{Bb:What notes?}}"
    }

    last_step = True

    def check_command(self):

        if self.last_user_input in self.extra_hints:
            self.send_hint(self.extra_hints[self.last_user_input])
            return

        return StepTemplateNano.check_command(self)

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    print_text = [
        "{{yb:How did you lock your front door?}}"
    ]
    story = [
        "Swordsmaster: {{Bb:There is a monster seeking what is locked away in that section. "
        "To unlock it would put the world in peril.}}",
        "",
        "{{yb:1: Do you know how to unlock it?}}",
        "{{yb:2: What is inside that is so dangerous?}}",
        "{{yb:3: This world is already in peril. People are disappearing.}}"
    ]

    commands = [
        "echo 3"
    ]
    # This logic for commands doesn't work
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    extra_hints = {
        "echo 1": "Swordsmaster: {{Bb:I was the one who locked it away. I will not unlock it for good reason.}}",
        "echo 2": "Swordsmaster: {{Bb:A command which gives the wielder tremendous power. "
                  "I was concerned what would happen if the command was put in the wrong hands.}}"
    }

    def check_command(self):

        if self.last_user_input in self.extra_hints:
            self.send_hint(self.extra_hints[self.last_user_input])

        return StepTemplateNano.check_command(self)

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    print_text = [
        "{{yb:This world is already in peril. People are disappearing.}}"
    ]
    story = [
        "Swordsmaster: {{Bb:I hoped something like this would never happen. Perhaps it is good then you are here. "
        + get_username() + ", do you know why I let you into my house?}}",
        "{{yb:1: No.}}",
        "{{yb:2: You knew my name?}}",
        "{{yb:3: You are a friendly individual?}}"
    ]
    extra_hints = {
        "echo 3": "Swordsmaster: {{Bb:No, my door is locked to most people.}}"
    }
    commands = [
        "echo 2",
        "echo 3"
    ]

    def check_command(self):
        if self.last_user_input in self.extra_hints:
            self.send_hint(self.extra_hints[self.last_user_input])

        return StepTemplateNano.check_command(self)


    def next(self):
        NextStep()


# "Swordsmaster: {{Bb:I used a special command. Only those who have "
# "proved themselves may learn it.",
# # How does he know your name? Initially thought of ls -l.
# "I know of your name...it is written all over this world for those "
# "who know where to look.",
# # ...but are you who you say you are? (Give user a test?)
# "...Ok. I will teach how I lock my door and protect myself.",
# "First, try and}} {{lb:go inside my basement.}}"
