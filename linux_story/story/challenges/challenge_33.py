#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_nano import TerminalNano


class StepTemplateNano(StepTemplate):
    TerminalClass = TerminalNano


class Step1(StepTemplateNano):
    story = [
        _("You are in a clearing. {{lb:Look around.}}"),
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Look around the clearing with}} {{yb:ls}}")
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
            "contents": get_story_file("x-sign")
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
            "contents": get_story_file("w-sign"),
        }
    ]

    def next(self):
        return 33, 2


class Step2(StepTemplateNano):
    story = [
        _("There's a house in the clearing. Have a {{lb:look}} in the {{lb:house}}, or try and {{lb:go inside}}."),
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
        _("{{rb:Use}} {{yb:ls house/}} {{rb:to look in the house.}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 33, 3


class Step3(StepTemplateNano):
    story = [
        _("Huh, you can't seem to look inside."),
        _("It is locked in the same way the {{bb:private-section}} in the library is."),
        _("Maybe there's a clue somewhere around here."),
        "",
        _("{{lb:Investigate}} the area and see if you can find any clues.")
    ]
    start_dir = "~/woods/clearing"

    # This should be an array of allowed directories you can end up in.
    # Perhaps an empty array means it doesn't matter where you end up.
    end_dir = "~/woods/clearing"

    hints = [
        _("{{rb:There is a signpost in the garden.}} {{lb:Examine}} {{rb:it.}}"),
        _("{{rb:Examine that signpost with}} {{yb:cat signpost}}{{rb:.}}")
    ]

    commands = [
        "cat signpost"
    ]

    # Perhaps a nice data structure could be if the list of commands were
    # paired with appropriate hints?
    paired_hints = {
        "ls": _("Try examining the individual items with {{lb:cat}}.")
    }

    def next(self):
        return 33, 4


class Step4(StepTemplateNano):
    story = [
        _("Okay, the signpost has an instruction on it. Let's try it out.")
    ]

    # It would be good if we could pass the current dir across and this would
    # simply be the default?
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    hints = [
        _("{{rb:Use}} {{yb:echo knock knock}} {{rb:to knock on the door.}}")
    ]

    commands = [
        "echo knock knock"
    ]

    def next(self):
        return 33, 5



class Step5(StepTemplateNano):
    story = [
        _("You hear a deep voice on the other side of the door."),
        "",
        _("Swordmaster:"),
        _("{{Bb:If you have me, you want to share me."),
        _("If you share me, you haven't got me."),
        _("What am I?}}"),
        "",
        _("{{yb:1. What?}}"),
        _("{{yb:2. I don't know}}")
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    def next(self):
        if self._last_user_input.lower() == "secret" or self._last_user_input.lower() == "echo secret":
            return 33, 6
        else:
            return 33, 8


class Step6(StepTemplateNano):
    story = [
        _("Swordmaster: {{Bb:...Did you complete the cave challenge?"),
        _("Fine, here's another. Unlock the door to my house.}}")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    def next(self):
        return 33, 7


class Step7(StepTemplateNano):
    story = [
        _("Swordmaster: {{Bb:I thought so. You need to complete the challenges}} {{lb:in the cave in the woods}}"),
        _("{{Bb:Come back when you've finished.}}")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/cave"
    hints = [
        _("Swordmaster: {{Bb:Head to the}} {{bb:~/woods/cave}} {{Bb:and stop hanging around outside my house!}}"),
        "",
        _("{{rb:Head to}} {{bb:~/woods/cave}}")
    ]

    def check_command(self, line):
        if line == "echo knock knock":
            self.send_hint("Swordmaster: {{Bb:Go and find the answer. Don't just stand there.}}")
            return
        return StepTemplateNano.check_command(self, line)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 33, 8


class Step8(StepTemplateNano):
    story = [
        _("Swordmaster: {{Bb:That is not the answer! Find the answer}} {{lb:in the cave near the woods.}}")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/cave"
    hints = [
        _("Swordmaster: {{Bb:Head to the}} {{bb:~/woods/cave}} {{Bb:and stop hanging around outside my house!}}"),
        _("{{rb:Head to}} {{bb:~/woods/cave}}")
    ]

    def check_command(self, line):
        if line == "echo knock knock":
            self.send_hint(_("Swordmaster: {{Bb:Go and find the answer. Don't just stand there guessing.}}"))
            return
        return StepTemplateNano.check_command(self, line)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 33, 9


class Step9(StepTemplateNano):
    story = [
        _("{{lb:You walk slowly into the cave. It has a musty smell.}}"),
        _("{{Bb:Look around.}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    def next(self):
        return 34, 1
