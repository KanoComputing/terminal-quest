#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.common import get_story_file
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.challenges.challenge_38 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateChmod(TerminalChmod):
    challenge_number = 37


class Step1(StepTemplateChmod):
    story = [
        "You set off the firework!",
        "{{gb:Congratulations, you learnt all the chmod commands.}}",
        "{{lb:Go back into the cave.}}"
    ]
    start_dir = "~/woods/cave/locked-room"
    end_dir = "~/woods/cave"
    hints = [
        "Use {{yb:cd ..}} to go back to the cave."
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "{{gb:Thunk.}}",
        "",
        "Something new landed in front of you.",
        "{{lb:Look around}} to see what it is."
    ]
    file_list = [
        {
            "path": "~/woods/cave/chest",
            "permissions": 0000,
            "type": "directory"
        },
        {
            "path": "~/woods/cave/chest/answer",
            "type": "file",
            "permissions": 0644,
            "contents": get_story_file("answer-cave")
        },
        {
            "path": "~/woods/cave/chest/riddle",
            "type": "file",
            "permissions": 0644,
            "contents": get_story_file("riddle-cave")
        }
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    hints = [
        "Use {{lb:ls}} to see what landed in front of you."
    ]
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "There is a {{bb:chest}} in front of you.",
        "{{lb:Look inside the chest.}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    hints = [
        "Use {{yb:ls chest}} to see inside the chest"
    ]
    commands = [
        "ls chest",
        "ls chest/"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "You can't see inside.",
        "It could be {{lb:it is missing all its permissions.}}",
        "Try and open it.",
        "{{lb:You need to combine the flags you learnt in the previous challenges.}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "chmod +rwx chest",
        "chmod +wxr chest",
        "chmod +xrw chest",
        "chmod +rxw chest",
        "chmod +xwr chest",
        "chmod +wrx chest",
        "chmod +rwx chest/",
        "chmod +wxr chest/",
        "chmod +xrw chest/",
        "chmod +rxw chest/",
        "chmod +xwr chest/",
        "chmod +wrx chest/"
    ]
    hints = [
        "Use {{yb:chmod +rwx chest}} to unlock the chest."
    ]

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = [
        "{{gb:You opened it!}}",
        "Now {{lb:look inside}} the chest."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"

    commands = [
        "ls chest",
        "ls chest/"
    ]

    hints = [
        "Use {{yb:ls chest/}} to look inside the chest."
    ]

    def next(self):
        Step6()


class Step6(StepTemplateChmod):
    story = [
        "You see a riddle, and an answer. {{lb:Examine}} them."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat chest/answer"
    ]
    hints = [
        "Use {{yb:cat chest/answer}} to examine the answer in the chest."
    ]

    def next(self):
        NextStep()
