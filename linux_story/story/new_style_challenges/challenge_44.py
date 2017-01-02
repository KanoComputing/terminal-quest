#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.IStep import IStep
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.new_terminals.terminal_rm import TerminalRm


class StepTemplateRm(IStep):
    TerminalClass = TerminalRm


class Step1(StepTemplateRm):
    story = [
        "You destroyed the note.",
        "",
        "It is time to find that rabbit.",
        "{{lb:Go to where you met the rabbit.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/woods/thicket"

    hints = [
        "",
        "{{lb:You met the rabbit in the}} {{bb:~/woods/thicket}}",
        "{{rb:Go to}} {{yb:~/woods/thicket}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 44, 2


class Step2(StepTemplateRm):
    story = [
        "{{lb:Look around.}}"
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    commands = [
        "ls",
        "ls .",
        "ls ./",
        "ls -a",
        "ls -a .",
        "ls -a ./"
    ]

    hint = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        return 44, 3


class Step3(StepTemplateRm):
    story = [
        "You are outside the rabbithole. Try and {{lb:go inside.}}"
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    dirs_to_attempt = "~/woods/thicket/rabbithole"

    commands = [
        "cd rabbithole",
        "cd rabbithole/"
    ]
    file_list = [
        {
            "type": "directory",
            "path": "~/woods/thicket/rabbithole",
            "permissions": 0000
        }
    ]

    hints = [
        "{{rb:Use}} {{yb:cd rabbithole}} {{rb:to go inside the rabbithole.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 44, 4


class Step4(StepTemplateRm):
    story = [
        "It looks like it is locked to us. The rabbit must have learnt how to lock the directory.",
        "",
        "{{lb:Unlock it.}}",
        "Use the same command you used to unlock the {{bb:private-section}}."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"

    commands = [
        "chmod +rwx rabbithole",
        "chmod +rwx rabbithole/",
        "chmod +rxw rabbithole",
        "chmod +rxw rabbithole/",
        "chmod +wxr rabbithole",
        "chmod +wxr rabbithole/",
        "chmod +wrx rabbithole",
        "chmod +wrx rabbithole/",
        "chmod +xwr rabbithole",
        "chmod +xwr rabbithole/",
        "chmod +xrw rabbithole",
        "chmod +xrw rabbithole/"
    ]

    hints = [
        "{{rb:Use}} {{yb:chmod +rwx rabbithole}}"
    ]

    def next(self):
        return 44, 5


class Step5(StepTemplateRm):
    story = [
        "{{lb:Go inside the rabbithole.}}"
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "cd rabbithole",
        "cd rabbithole/"
    ]

    file_list = [
        {
            "path": "~/woods/thicket/rabbithole/bell",
            "type": "file",
            "contents": get_story_file("bell"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/Rabbit",
            "type": "file",
            "contents": get_story_file("Rabbit"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Mum",
            "type": "file",
            "contents": get_story_file("Mum"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Dad",
            "type": "file",
            "contents": get_story_file("Dad"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/dog",
            "type": "file",
            "contents": get_story_file("dog"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Edith",
            "type": "file",
            "contents": get_story_file("Edith"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Edward",
            "type": "file",
            "contents": get_story_file("Edward"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/grumpy-man",
            "type": "file",
            "contents": get_story_file("grumpy-man"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Mayor",
            "type": "file",
            "contents": get_story_file("Mayor"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/young-girl",
            "type": "file",
            "contents": get_story_file("young-girl"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/little-boy",
            "type": "file",
            "contents": get_story_file("little-boy"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/swordmaster",
            "contents": get_story_file("swordmaster-without-sword"),
            "type": "file",
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/torn-note",
            "contents": get_story_file("torn-note")
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/torn-scroll",
            "contents": get_story_file("torn-sudo")
        }
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 45, 1
