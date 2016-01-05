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
from linux_story.story.challenges.challenge_38 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 37


class Step1(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Now try again. Move the}} {{lb:key.sh}} "
        "{{Bb:outside the basement.}}"
    ]
    commands = [
        "mv key.sh ../",
        "mv key.sh .."
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    commands = [
        "mv key.sh ../",
        "mv key.sh .."
    ]

    hints = [
        "{{rb:Use}} {{yb:mv key.sh ../}} {{rb:to move the key.sh}} "
        "{{rb:back a directory.}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Leave the basement and join me.}}"
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:cd ../}} {{rb:to go back a directory.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Now finally, make the key executable with}} "
        "{{yb:chmod +x key.sh}} {{Bb:so you can run it.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:chmod +x key.sh}} {{rb:to activate the key.}}"
    ]
    commands = [
        "chmod +x key.sh"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:If you look around now, you can see the key has been activated.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Look around with}} {{yb:ls}} {{rb:to see that the key has been activated.}}"
    ]
    commands = [
        "ls",
        "ls -l"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:The key.sh is now a bright green. This means you can use it.}}",
        "{{Bb:Try using the key with}} {{yb:./key.sh}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:./key.sh}}"
    ]
    commands = [
        "./key.sh"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Thank you, you locked the basement back up for me.}}",
        "{{Bb:Well done - you've learned to use chmod!}}",
        "{{Bb:...}}",
        "{{Bb:...}}",
        "{{Bb:...what is this?}}",
        "{{Bb:Do you see this? Have a}} {{lb:look around}}."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "ls",
        "ls -a"
    ]

    story_dict = {
        "note_swordsmaster-house": {
            "path": "~/woods/clearing/house",
            "name": "note"
        }
    }

    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        NextStep()
