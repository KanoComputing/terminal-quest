#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.IStep import IStep
from linux_story.common import get_story_file
from linux_story.helper_functions import wrap_in_box
from linux_story.story.new_terminals.terminal_chmod import TerminalChmod
from linux_story.story.new_terminals.terminal_rm import TerminalRm


class StepTemplateChmod(IStep):
    TerminalClass = TerminalChmod


class StepTemplateRm(IStep):
    TerminalClass = TerminalRm


REPLY_PRINT_TEXT = "{{yb:A rabbit came and stole the command in front of us.}}"


class Step1(StepTemplateChmod):
    story = [
        "You are standing alone in the library. The rabbit has stolen the command, and you have an increased sense of "
        "impending doom.",
        "The swordmaster runs into the room.",
        "Swordmaster: {{Bb:What have you done?}}",
        "",
        "{{yb:1:}}" + REPLY_PRINT_TEXT,
        "{{yb:2: Nothing.}}"
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
        "Swordmaster: {{Bb:Speak with}} {{lb:echo}} {{Bb:and tell me!}}"
    ]

    def next(self):
        if self._last_user_input == "echo 2":
            return 43, 100
        else:
            return 43, 2


class Step100(StepTemplateChmod):
    story = [
        "Swordmaster: {{rb:ENOUGH!}}",
        "{{Bb:Tell me}} {{rb:the truth.}}",
        "{{Bb:You need my help to fix this....}}",
        "",
        "{{yb:1:}}" + REPLY_PRINT_TEXT,
        "{{yb:2: Nothing.}}"
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    hints = [
        "{{rb:Tell the swordmaster the truth, using}} {{yb:echo 1}}"
    ]

    def check_command(self, last_user_input):
        if last_user_input == "echo 2":
            self.send_hint("Swordmaster: {{Bb:We both know that's not true....}}")
            return
        return StepTemplateChmod.check_command(self, last_user_input)

    def next(self):
        return 43, 2


class Step2(StepTemplateChmod):
    print_text = [REPLY_PRINT_TEXT]
    story = [
        "Swordmaster: {{Bb:I see.}}",
        "{{Bb:I frequently see a white rabbit around my place. It must live close to my house.}}",
        "{{Bb:It always seemed innocent before. I wonder what has changed?}}",
        "{{Bb:Perhaps he is}} {{lb:possessed}}{{Bb:.}}",
        "",
        "{{Bb:We must remove the source of the problem. I will teach you how to.}}",
        "",
        "{{pb:Ding. Dong.}}",
        "",
        "You heard the a bell. {{lb:Look around.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]
    hints = [
        "Look around with {{yb:ls}}"
    ]
    file_list = [
        {
            "path": "~/town/east/library/private-section/sword",
            "contents": get_story_file("RM-sword"),
            "type": "file",
            "permissions": 0644
        }
    ]

    deleted_items = ["~/town/east/library/private-section/swordmaster"]

    def next(self):
        return 43, 3


class Step3(StepTemplateChmod):
    story = [
        "The swordmaster has gone.",
        "",
        "He left something behind. It looks like the {{lb:sword}} he carries around with him.",
        "{{lb:Examine}} it."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "cat sword"
    ]

    hints = [
        "{{rb:Use}} {{yb:cat sword}} {{rb:to examine it.}}"
    ]

    def next(self):
        return 43, 4


class Step4(StepTemplateRm):
    story = [
        "It has a command inscribed on it.",
        "....{{lb:rm}}...?"
    ]

    story += wrap_in_box([
        _("{{gb:New Spell:}} Use {{yb:rm}} to"),
        _(" {{lb:remove an item}}.")
    ])

    story += [
        "Use {{yb:rm note}}, to test the command out on the note.",
        "Be careful though....it looks dangerous."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "rm note"
    ]
    highlighted_commands = ["rm"]

    hints = [
        "",
        "{{rb:Use the command}} {{yb:rm note}}"
    ]

    def next(self):
        return 43, 5


class Step5(StepTemplateRm):
    story = [
        "{{lb:Look around.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls"
    ]

    hints = [
        "Use the command {{lb:ls}}"
    ]

    def next(self):
        return 44, 1
