#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file, get_username
from linux_story.story.terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        _("You see a Masked Swordmaster watching you."),
        _("{{lb:Listen}} to what he has to say.")
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        _("{{rb:Use}} {{yb:cat Swordmaster}} {{rb:to}} {{lb:listen}} {{rb:to what the Swordmaster has to say.}}")
    ]
    commands = [
        "cat Swordmaster"
    ]

    def next(self):
        return 39, 2


class Step2(StepTemplateChmod):
    story = [
        _("{{wb:Swordmaster:}} {{Bb:\"Child, why do you seek me?\"}}"),
        "",
        _("{{yb:1: I want to unlock the private section in the library.}}"),
        _("{{yb:2: Who are you?}}"),
        _("{{yb:3: Have you been leaving me strange notes?}}"),
        "",
        _("Respond with {{yb:echo 1}}, {{yb:echo 2}}, or {{yb:echo 3}}.")
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    extra_hints = {
        "echo 2": _("Swordmaster: {{Bb:\"I have fled the outside world to make my home here in this peaceful wood. "
                    "The few who know of me call me the Masked Swordmaster.\"}}"),
        "echo 3": _("Swordmaster: {{Bb:\"What notes?\"}}")
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
        _("{{yb:I want to unlock the private section in the library.}}")
    ]
    story = [
        _("Swordmaster: {{Bb:\"Well, if you unlocked the chest in the}} {{bb:~/woods/cave}}"
        "{{Bb:, then you already know how.}}\""),
        _("{{Bb:\"A note of caution: what is inside is both powerful and dangerous.\"}}"),
        "",
        _("{{yb:1: What is inside the library that is so dangerous?}}"),
        _("{{yb:2: Why do you live so far from other people?}}"),
        _("{{yb:3: Do you know why people are disappearing?}}")
    ]

    commands = [
        "echo 3"
    ]

    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    extra_hints = {
        "echo 1": _("Swordmaster: \"A command that gives the wielder tremendous power, "
                    "turning you into a Super User.\"}}"),
        "echo 2": _("Swordmaster: {{Bb:\"Being a swordmaster, I have the ability to}} {{lb:remove}} {{Bb:others. "
                    "This makes people uneasy around me, so I choose to live in the woods instead.\"}}")
    }

    def check_command(self, line):
        if line in self.extra_hints:
            self.send_hint(self.extra_hints[line])

        return StepTemplateChmod.check_command(self, line)

    def next(self):
        return 39, 4


class Step4(StepTemplateChmod):
    print_text = [
        _("{{yb:Do you know why people are disappearing?}}")
    ]
    story = [
        _("Swordmaster: {{Bb:\"I wasn't aware people were disappearing. Is that what is causing that bell?"),
        _("Perhaps it is good you are here then.\""),
        _("\"Tell me, what is your name?\"}}")
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "echo " + get_username()
    ]
    hints = [
        _("{{rb:Use}} {{yb:echo " + get_username() + "}} {{rb:to give your name.}}")
    ]

    def check_command(self, last_user_input):
        if last_user_input.startswith("echo") and last_user_input not in self.commands:
            self.send_hint(
                _("Swordmaster: {{Bb:\"That's a strange name. Is that really your name?\"}}")
            )
        return StepTemplateChmod.check_command(self, last_user_input)

    def next(self):
        return 39, 5


class Step5(StepTemplateChmod):
    story = [
        _("Swordmaster: {{Bb:\"I thought you might be. Few have the power to use the commands you used earlier."),
        _("How did I know your name? Use}} {{yb:ls -l}} {{Bb:to see.\"}}")
    ]
    commands = [
        "ls -l",
        "ls -l .",
        "ls -l ./"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

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
        _("Swordmaster: {{Bb:\"Your name is written in this world, for anyone who knows where to look.\"}}"),
        "{{Bb:\"...\"}}",
        _("{{Bb:\"...why is there a}} {{lb:note}} {{Bb:in this room?\"}}"),
        _("{{Bb:\"Do you see it? Use}} {{lb:cat note}} {{Bb:to examine it.\"}}")
    ]
    commands = [
        "cat note"
    ]

    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    def next(self):
        return 40, 1
