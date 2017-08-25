#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        _("Swordsmaster:{{Bb:\"...this is very strange. I left the door open. Perhaps someone...or "
          "something...sneaked in while we were talking.\"}}"),
        _("{{Bb:\"You may need my help later. Come back if you are blocked by lack of knowledge.\"}}"),
        "",
        _("Time to head off - {{lb:leave}} the Swordmaster's house.")
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing"

    hints = [
        _("{{rb:Leave the house with}} {{yb:cd ..}}")
    ]

    file_list = [
        {
            "contents": get_story_file("note_woods"),
            "path": "~/woods/note",
            "permissions": 0644,
            "type": "file"
        },
        {
            "contents": get_story_file("Rabbit"),
            "path": "~/woods/thicket/Rabbit",
            "permissions": 0644,
            "type": "file"
        },
        {
            "path": "~/woods/thicket/rabbithole",
            "permissions": 0755,
            "type": "directory"
        },
        {
            "contents": get_story_file("note_swordsmaster-clearing"),
            "path": "~/woods/clearing/note",
            "permissions": 0644,
            "type": "file"
        },
        {
            "contents": get_story_file("note_rabbithole"),
            "path": "~/woods/thicket/note",
            "permissions": 0644,
            "type": "file"
        }
    ]

    def block_command(self, line):
        unblock_cd_commands(line)

    def next(self):
        return 40, 2


class Step2(StepTemplateChmod):
    story = [
        _("{{lb:Look around}} and see if there are clues about where to go next.")
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls -a"
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    def next(self):
        return 40, 3


class Step3(StepTemplateChmod):
    story = [
        _("Another note! What does this say?")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "cat note"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}")
    ]

    def next(self):
        return 40, 4


class Step4(StepTemplateChmod):
    story = [
        _("It looks like we should leave the clearing."),
        _("{{lb:Go back into the woods.}}")
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods"

    hints = [
        _("{{rb:Go back to the woods with}} {{yb:cd ../}}")
    ]

    def block_command(self, line):
        unblock_cd_commands(line)

    def next(self):
        return 40, 5


class Step5(StepTemplateChmod):
    story = [
        _("{{lb:Look around.}}")
    ]
    start_dir = "~/woods"
    end_dir = "~/woods"
    commands = [
        "ls",
        "ls -a"
    ]

    # This text is used so much we can probably save it as "default ls hint"
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    def next(self):
        return 40, 6


class Step6(StepTemplateChmod):
    story = [
        _("There's another note! {{lb:Read}} it.")
    ]
    start_dir = "~/woods"
    end_dir = "~/woods"
    commands = [
        "cat note"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat note}} {{rb:to examine the note.}}")
    ]

    def next(self):
        return 40, 7


class Step7(StepTemplateChmod):
    story = [
        _("Let's {{lb:go}} into the thicket.")
    ]
    start_dir = "~/woods"
    end_dir = "~/woods/thicket"
    hints = [
        _("{{rb:Use}} {{yb:cd thicket}} {{rb:to go into the thicket.}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 40, 8


class Step8(StepTemplateChmod):
    story = [
        _("You push through into a dense patch of plants. The trees overshadow you."),
        _("{{lb:Look around.}}")
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    def next(self):
        return 41, 1

