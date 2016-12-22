#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.common import get_story_file
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.challenges.challenge_34 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 33


class Step1(StepTemplateNano):
    story = [
        "You are in a clearing. {{lb:Look around.}}",
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Look around the clearing with}} {{yb:ls}}"
    ]

    file_list = [
        {
            "path": "~/woods/cave/sign",
            "permissions": 0644,
            "type": "file",
            "contents": get_story_file("sign_cave")
        },

        {
            "path": "~/woods/cave/dark-room",
            "permissions": 0300,
            "type": "directory"
        },
        {
            "path": "~/woods/cave/dark-room/sign",
            "permissions": 0644,
            "type": "file",
            "contents": get_story_file("w-sign")
        },

        {
            "path": "~/woods/cave/cage",
            "permissions": 0500,
            "type": "directory"
        },
        {
            "path": "~/woods/cave/cage/bird",
            "permissions": 0644,
            "type": "file",
            "contents": get_story_file("bird")
        },
        {
            "path": "~/woods/cave/cage/sign",
            "permissions": 0644,
            "type": "file",
            "contents": get_story_file("r-sign")
        },

        {
            "path": "~/woods/cave/locked-room/",
            "permissions": 0600,
            "type": "directory"
        },
        {
            "path": "~/woods/cave/locked-room/lighter",
            "permissions": 0644,
            "type": "file",
            "contents": get_story_file("lighter")
        },
        {
            "path": "~/woods/cave/locked-room/sign",
            "permissions": 0644,
            "type": "file",
            "contents": get_story_file("instructions-locked-room")
        }
    ]

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "There's a house in the clearing. Have a {{lb:look}} in the {{lb:house}}, or try and {{lb:go inside}}.",
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    dirs_to_attempt = "~/woods/clearing/house"
    commands = [
        "ls house",
        "ls house/",
        "ls -a house",
        "ls -a house/",
        "cd house",
        "cd house/"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls house/}} {{rb:to look in the house.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Huh, you can't seem to look inside.",
        "It is locked in the same way the {{bb:private-section}} in the library is.",
        "Maybe there's a clue somewhere around here.",
        "",
        "{{lb:Investigate}} the area and see if you can find any clues."
    ]
    start_dir = "~/woods/clearing"

    # This should be an array of allowed directories you can end up in.
    # Perhaps an empty array means it doesn't matter where you end up.
    end_dir = "~/woods/clearing"

    hints = [
        "{{rb:Examine that signpost with}} {{yb:cat signpost}}{{rb:.}}"
    ]

    commands = [
        "cat signpost"
    ]

    # Perhaps a nice data structure could be if the list of commands were
    # paired with appropriate hints?
    paired_hints = {
        "ls": "Try examining the individual items with {{lb:cat}}."
    }

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "So the signpost has an instruction on it? Let's carry it out."
    ]

    # It would be good if we could pass the current dir across and this would
    # simply be the default?
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    hints = [
        "{{rb:Use}} {{yb:echo knock knock}} {{rb:to knock on the door.}}"
    ]

    commands = [
        "echo knock knock"
    ]

    def next(self):
        Step5()



class Step5(StepTemplateNano):
    story = [
        "You hear a deep voice on the other side of the door.",
        "",
        "Swordmaster:",
        "{{Bb:If you have me, you want to share me.",
        "If you share me, you haven't got me.",
        "What am I?}}",
        "",
        "{{yb:1. What?}}",
        "{{yb:2. I don't know}}"
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    def next(self):
        if self.last_user_input.lower() == "secret" or self.last_user_input.lower() == "echo secret":
            Step5b()
        else:
            Step6()


class Step5b(StepTemplateNano):
    story = [
        "Swordmaster: {{Bb:...Did you complete the cave challenge?",
        "Fine, here's another. Unlock the door to my house.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    def next(self):
        Step5c()


class Step5c(StepTemplateNano):
    story = [
        "Swordmaster: {{Bb:I thought so. You need to complete the challenges}} {{lb:in the cave in the woods}}",
        "{{Bb:Come back when you've finished.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/cave"
    hints = [
        "Swordmaster: {{Bb:Head to the}} {{bb:~/woods/cave}} {{Bb:and stop hanging around outside my house!}}",
        "{{yb:Head to}} {{bb:~/woods/cave}}"
    ]

    def check_command(self):
        if self.last_user_input == "echo knock knock":
            self.send_hint("Swordmaster: {{Bb:Go and find the answer. Don't just stand there.}}")
            return
        return StepTemplateNano.check_command(self)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step6()


class Step6(StepTemplateNano):
    story = [
        "Swordmaster: {{Bb:That is not the answer! Find the answer}} {{lb:in the cave near the woods.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/cave"
    hints = [
        "Swordmaster: {{Bb:Head to the}} {{bb:~/woods/cave}} {{Bb:and stop hanging around outside my house!}}",
        "{{yb:Head to}} {{bb:~/woods/cave}}"
    ]

    def check_command(self):
        if self.last_user_input == "echo knock knock":
            self.send_hint("Swordmaster: {{Bb:Go and find the answer. Don't just stand there guessing.}}")
            return
        return StepTemplateNano.check_command(self)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step7()


class Step7(StepTemplateNano):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        NextStep()
