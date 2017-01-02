#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.IStep import IStep
from linux_story.common import get_story_file, get_username
from linux_story.story.new_terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(IStep):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "You see a Masked Swordmaster watching you.",
        "Listen to what he has to say."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:cat swordmaster}} {{rb:to}} {{lb:listen}} "
        "{{rb:to what the swordmaster has to say.}}"
    ]
    commands = [
        "cat swordmaster"
    ]

    def next(self):
        return 39, 2


class Step2(StepTemplateChmod):
    story = [
        "{{wb:Swordmaster:}} {{Bb:Child, why do you seek me?}}",
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
        "echo 2": "Swordmaster: {{Bb:I am one who has removed themselves from society. The few who know of me call me the Masked Swordmaster.}}",
        "echo 3": "Swordmaster: {{Bb:What notes?}}"
    }

    last_step = True

    def check_command(self, line):
        if line in self.extra_hints:
            self.send_hint(self.extra_hints[line])
            return

        return StepTemplateChmod.check_command(self, line)

    def next(self):
        return 39, 3


class Step3(StepTemplateChmod):
    print_text = [
        "{{yb:I want to unlock the private section in the library.}}"
    ]
    story = [
        "Swordmaster: {{Bb:Well, if you unlocked the chest in the}} {{lb:~/woods/cave}}"
        "{{Bb:, then you already know how.}}",
        "{{Bb:A note of caution: what is inside is both powerful and dangerous.}}"
        "",
        "{{yb:1: What is inside the library that is so dangerous?}}",
        "{{yb:2: Why do you live so far from other people?}}",
        "{{yb:3: Do you know why people are disappearing?}}"
    ]

    commands = [
        "echo 3"
    ]

    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    extra_hints = {
        "echo 1": "Swordmaster: {{Bb:A command that makes the wielder into a Super User and gives them tremendous power.}}",
        "echo 2": "Swordmaster: {{Bb:Being a swordmaster, I have the ability to}} {{lb:remove}} {{Bb:others. "
                  "This makes people uneasy around me, so I choose to live in the woods instead.}}"
    }

    def check_command(self, line):
        if line in self.extra_hints:
            self.send_hint(self.extra_hints[line])

        return StepTemplateChmod.check_command(self, line)

    def next(self):
        return 39, 4


class Step4(StepTemplateChmod):
    print_text = [
        "{{yb:Do you know why people are disappearing?}}"
    ]
    story = [
        "Swordmaster: {{Bb:I wasn't aware people were disappearing. Is that what is causing that bell?",
        "Perhaps it is good you are here then.",
        "Tell me, what is your name?}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "echo " + get_username()
    ]
    hints = [
        "{{rb:Use}} {{yb:echo " + get_username() + "}} {{rb:to give your name.}}"
    ]

    def check_command(self, last_user_input):
        if last_user_input.startswith("echo") and last_user_input not in self.commands:
            self.send_hint("Swordmaster: {{Bb:That's a strange name. Is that really your name?}}")
            return
        return StepTemplateChmod.check_command(self, last_user_input)

    def next(self):
        return 39, 5


class Step5(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:I thought you might be. Few have the power to use the commands you used earlier.",
        "How did I know your name? Use}} {{yb:ls -l}} {{Bb:to see.}}"
    ]
    commands = [
        "ls -l"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "Swordmaster: {{Bb:Use}} {{yb:ls -l}} {{Bb:}}"
    ]

    file_list = [
        {
            "contents": get_story_file("note_swordsmaster-house"),
            "path": "~/woods/clearing/house/note",
            "permissions": 0644,
            "type": "file"
        }
    ]

    def next(self):
        return 39, 6


class Step6(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:Your name is written in this world, for anyone who knows where to look.}}",
        "{{Bb:...}}",
        "{{Bb:...why is there a}} {{lb:note}} {{Bb:in this room?}}",
        "{{Bb:Do you see it? Use}} {{lb:cat note}} {{Bb:to examine it.}}"
    ]
    commands = [
        "cat note"
    ]

    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    def next(self):
        return 40, 1
