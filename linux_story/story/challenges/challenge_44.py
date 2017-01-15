#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.PlayerLocation import generate_real_path
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.file_creation.FileTree import modify_permissions
from linux_story.helper_functions import has_write_permissions, has_read_permissions, has_execute_permissions
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_rm import TerminalRm


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm


class Step1(StepTemplateRm):
    story = [
        _("You destroyed the note."),
        "",
        _("It is time to find that rabbit."),
        _("{{lb:Go to where you met the rabbit.}}")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/woods/thicket"

    hints = [
        "",
        _("{{lb:You met the rabbit in the}} {{bb:~/woods/thicket}}"),
        _("{{rb:Use}} {{yb:cd ~/woods/thicket}}")
    ]
    dark_theme = True

    file_list = [
        {
            "path": "~/town/east/library/rabbithole/swordmaster",
            "contents": get_story_file("swordmaster"),
            "permissions": 0644,
            "type": "file"
        }
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 44, 2


class Step2(StepTemplateRm):
    story = [
        _("{{lb:Look around.}}")
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

    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]
    dark_theme = True

    def next(self):
        return 44, 3


class Step3(StepTemplateRm):
    story = [
        _("You are outside the rabbithole. It has a large boulder in front of it."),
        _("Try and {{lb:go inside.}}")
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    dirs_to_attempt = "~/woods/thicket/rabbithole"

    commands = [
        "cd rabbithole",
        "cd rabbithole/"
    ]

    hints = [
        _("{{rb:Use}} {{yb:cd rabbithole}} {{rb:to go inside the rabbithole.}}")
    ]
    dark_theme = True

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 44, 4


class Step4(StepTemplateRm):
    story = [
        _("You cannot get past the boulder."),
        _("The {{bb:rabbithole}} is completely inaccessible."),
        "",
        _("{{lb:Unlock it.}}"),
        _("Use the same command you used to unlock the {{bb:private-section}}.")
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"

    hints = [
        _("{{rb:Use}} {{yb:chmod +rwx rabbithole/}}")
    ]
    dark_theme = True

    def check_command(self, line):
        dir = generate_real_path("~/woods/thicket/rabbithole")
        if has_write_permissions(dir) and has_read_permissions(dir) and has_execute_permissions(dir):
            return True
        self.send_stored_hint()

    def next(self):
        return 44, 5


class Step5(StepTemplateRm):
    story = [
        _("You pushed the boulder aside."),
        _("{{lb:Go inside the rabbithole.}}")
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "cd rabbithole",
        "cd rabbithole/"
    ]
    hints = [
        "{{rb:Use}} {{yb:cd rabbithole}} {{rb:to go inside the rabbithole.}}"
    ]
    dark_theme = True

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
            "contents": get_story_file("grumpy-man-fixed"),
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
            "path": "~/woods/thicket/rabbithole/cage/Swordmaster",
            "contents": get_story_file("swordmaster-without-sword"),
            "type": "file",
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/chest/torn-note",
            "contents": get_story_file("torn-note")
        },
        {
            "path": "~/woods/thicket/rabbithole/chest/torn-scroll",
            "contents": get_story_file("torn-sudo")
        }
    ]

    def _run_after_text(self):
        modify_permissions("~/woods/thicket/rabbithole/cage", 0500)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 45, 1
