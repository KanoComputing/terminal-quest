#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.file_creation.FileTree import modify_permissions
from linux_story.helper_functions import wrap_in_box
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.terminals.terminal_rm import TerminalRm


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm


REPLY_PRINT_TEXT = _("{{yb:A rabbit came and stole the command in front of me.}}")


class Step1(StepTemplateChmod):
    story = [
        _("You are standing alone in the library. The rabbit has stolen the command, and you have an "
          "increased sense of impending doom."),
        _("The swordmaster runs into the room."),
        "",
        _("Swordmaster: {{Bb:What have you done?}}"),
        "",
        "{{yb:1:}} " + REPLY_PRINT_TEXT,
        _("{{yb:2: Nothing.}}")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    file_list = [
        {
            "path": "~/town/east/library/private-section/swordmaster",
            "contents": get_story_file("swordmaster"),
            "permissions": 0644,
            "type": "file"
        }
    ]
    commands = [
        "echo 1",
        "echo 2"
    ]
    hints = [
        _("Swordmaster: {{Bb:Speak with}} {{lb:echo}} {{Bb:and tell me!}}")
    ]
    dark_theme = True

    def _run_at_start(self):
        modify_permissions("~/woods/thicket/rabbithole", 0000)

    def next(self):
        if self._last_user_input == "echo 2":
            return 43, 100
        else:
            return 43, 2


class Step100(StepTemplateChmod):
    story = [
        _("Swordmaster: {{rb:ENOUGH!}}"),
        _("{{Bb:Tell me}} {{rb:the truth.}}"),
        _("{{Bb:You need my help to fix this....}}"),
        "",
        _("{{yb:1:}} " + REPLY_PRINT_TEXT),
        _("{{yb:2: Nothing.}}")
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    hints = [
        _("{{rb:Tell the swordmaster the truth, using}} {{yb:echo 1}}")
    ]
    dark_theme = True

    def check_command(self, last_user_input):
        if last_user_input == "echo 2":
            self.send_hint(
                _("Swordmaster: {{Bb:We both know that's not true....}}")
            )
            return
        return StepTemplateChmod.check_command(self, last_user_input)

    def next(self):
        return 43, 2


class Step2(StepTemplateChmod):
    print_text = [REPLY_PRINT_TEXT]
    story = [
        _("Swordmaster: {{Bb:I see.}}"),
        _("{{Bb:I frequently see a white rabbit around my place. It must live close to my house.}}"),
        _("{{Bb:It always seemed innocent before. I wonder what has changed?}}"),
        _("{{Bb:Perhaps he is}} {{lb:possessed}}{{Bb:.}}"),
        "",
        _("{{Bb:We must remove the source of the problem. I will teach you how.}}"),
        "",
        _("{{pb:Ding. Dong.}}"),
        "",
        _("You heard the a bell. {{lb:Look around.}}")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]
    hints = [
        _("{{rb:Look around with}} {{yb:ls}}")
    ]
    file_list = [
        {
            "path": "~/town/east/library/private-section/sword",
            "contents": get_story_file("RM-sword"),
            "type": "file",
            "permissions": 0644
        }
    ]
    dark_theme = True

    deleted_items = ["~/town/east/library/private-section/swordmaster"]

    def next(self):
        return 43, 3


class Step3(StepTemplateChmod):
    story = [
        _("The swordmaster has gone."),
        "",
        _("He left something behind. It looks like the {{lb:sword}} he carries around with him."),
        _("{{lb:Examine}} it.")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "cat sword"
    ]
    dark_theme = True

    hints = [
        _("{{rb:Use}} {{yb:cat sword}} {{rb:to examine it.}}")
    ]

    def next(self):
        return 43, 4


class Step4(StepTemplateRm):
    story = [
        _("It has a command inscribed on it."),
        "....{{lb:rm}}...?"
    ]

    story += wrap_in_box([
        _("{{gb:New Spell:}} Use {{yb:rm}} to"),
        _(" {{lb:remove an item}}.")
    ])

    story += [
        _("Use {{yb:rm note}}, to test the command out on the note."),
        _("Be careful though....it looks dangerous.")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "rm note"
    ]
    highlighted_commands = ["rm"]

    hints = [
        "",
        _("{{rb:Use the command}} {{yb:rm note}}")
    ]
    dark_theme = True

    def next(self):
        return 43, 5


class Step5(StepTemplateRm):
    story = [
        _("{{lb:Look around.}}")
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls"
    ]

    hints = [
        _("{{rb:Use the command}} {{yb:ls}}")
    ]
    dark_theme = True

    def next(self):
        return 44, 1
