#!/usr/bin/env python
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
import time
from threading import Thread

from linux_story.Animation import Animation
from linux_story.IStep import IStep
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.new_terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(IStep):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "Now, which is the locked room? {{lb:Look around}} to remind yourself."
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    file_list = [
        {
            "path": "~/town/east/library/Rabbit",
            "contents": get_story_file("Rabbit"),
            "permissions": 0644,
            "type": "file"
        }
    ]
    deleted_items = [
        "~/woods/thicket/Rabbit",
        "~/woods/thicket/note"
    ]

    def next(self):
        return 42, 2


class Step2(StepTemplateChmod):
    story = [
        "Ah, it's the {{lb:private-section}}.",
        "The Rabbit looks very excited. His eyes are sparkling.",
        "",
        "Unlock the {{lb:private-section}}."
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"
    commands = [
        "chmod +rwx private-section",
        "chmod +rwx private-section/",
        "chmod +wxr private-section",
        "chmod +wxr private-section/",
        "chmod +xrw private-section",
        "chmod +xrw private-section/",
        "chmod +rxw private-section",
        "chmod +rxw private-section/",
        "chmod +xwr private-section",
        "chmod +xwr private-section/",
        "chmod +wxr private-section",
        "chmod +wxr private-section/"
    ]

    hints = [
        "{{rb:The command is}} {{yb:chmod +rwx private-section}} {{rb:to "
        "enable all the permissions.}}"
    ]

    def next(self):
        return 42, 3


class Step3(StepTemplateChmod):
    story = [
        "Awesome, you unlocked it! {{lb:Go inside the private-section.}}"
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library/private-section"
    hints = [
        "{{rb:Use}} {{yb:cd private-section/}} {{rb:to go inside.}}"
    ]
    file_list = [
        {
            "path": "~/town/east/library/private-section/chest/scroll",
            "contents": get_story_file("SUDO"),
            "permissions": 0644,
            "type": "file"
        },
        {
            "path": "~/town/east/library/private-section/chest/torn-note",
            "contents": get_story_file("torn-note"),
            "permissions": 0644,
            "type": "file"
        }
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 42, 4


class Step4(StepTemplateChmod):
    story = [
        "Have a {{lb:look around.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls",
        "ls -a",
        "cat chest/scroll",
        "cat chest/torn-note",
        "ls chest",
        "ls chest/",
        "ls chest/scroll",
        "ls chest/torn-note"
    ]
    file_list = [
        {
            "path": "~/town/east/library/private-section/Rabbit",
            "contents": get_story_file("Rabbit"),
            "permissions": 0644,
            "type": "file"
        }
    ]
    deleted_items = ["~/town/east/library/Rabbit"]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def block_command(self, line):
        if line == "cat chest/scroll":
            self.set_last_user_input(line)
            print "The Rabbit snatched the chest away!"
            return True
        return StepTemplateChmod.block_command(self, line)

    def check_command(self, line):
        if self.get_last_user_input() == "cat chest/scroll":
            return True
        return StepTemplateChmod.check_command(self, line)

    def next(self):
        if self.get_last_user_input() == "cat chest/scroll":
            return 42, 5
        else:
            return 42, 6


class RabbitTakesChest(StepTemplateChmod):

    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    deleted_items = [
        "~/town/east/library/private-section/Rabbit",
        "~/town/east/library/private-section/chest"
    ]

    def next(self):
        return 42, 7


class Step5(RabbitTakesChest):
    story = [
        "You try and examine the contents of the chest, but the Rabbit snatches it and runs off!"
    ]


class Step6(RabbitTakesChest):
    story = [
        "You see a {{bb:chest}}.",
        "This looks like the treasure we were looking for.",
        "The Rabbit looks more excited than you've ever seen him before.",
        "He snatches the chest and runs off!"
    ]


class Step7(StepTemplateChmod):
    story = [
        "A {{bb:note}} flutters in front of you. {{lb:Read it.}}"
    ]

    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    commands = [
        "cat note"
    ]

    hints = [
        "{{rb:Read the note with}} {{yb:cat note}}"
    ]

    file_list = [
        {
            "contents": get_story_file("note_private-section"),
            "path": "~/town/east/library/private-section/note"
        }
    ]

    def _run_at_start(self):
        Animation("rabbit-animation").play_across_screen(speed=10)

    def next(self):
        return 42, 8


class Step8(StepTemplateChmod):
    story = [
        "The place shivers...and then everything goes black."
    ]

    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    def _run_at_start(self):
        t = Thread(target=self.__timeout_dark_theme)
        t.start()

    def __timeout_dark_theme(self):
        time.sleep(1)
        self.send_dark_theme()

    def next(self):
        return 43, 1

