# challenge_9.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
from linux_story.story.terminals.terminal_cd import TerminalCd


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        _("Oh no! Check your {{bb:Mum}} is alright.\n"),
        _("Type {{yb:cd ..}} to leave {{bb:town}}.")
    ]
    start_dir = "~/town"
    end_dir = "~"
    commands = ["cd ..", "cd ../", "cd"]
    hints = [_("{{rb:Use}} {{yb:cd ..}} {{rb:to start heading back home.}}")]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 9, 2


class Step2(StepTemplateCd):
    story = [
        _("{{pb:Ding. Dong.}}\n"),
        _("Type {{yb:cd my-house/kitchen}} to go straight to the {{bb:kitchen}}.\n"),
        _("{{gb:Press}} {{ob:TAB}} {{gb:to speed up your typing!}}")
    ]
    start_dir = "~"
    end_dir = "~/my-house/kitchen"
    commands = ["cd my-house/kitchen", "cd my-house/kitchen/"]
    hints = [
        _("{{rb:Use}} {{yb:cd my-house/kitchen}} {{rb:to go to the kitchen.}}")
    ]
    file_list = [
        {
            "path": "~/my-house/kitchen/note",
            "contents": get_story_file("note_kitchen"),
            "type": "file"
        }
    ]
    deleted_items = ['~/my-house/kitchen/Mum', '~/town/note']

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 9, 3


class Step3(StepTemplateCd):
    story = [
        _("Take a {{lb:look around}} to make sure everything is OK.")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = "ls"
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to see that everything is where it should be.}}")
    ]

    def next(self):
        return 9, 4


class Step4(StepTemplateCd):
    story = [
        _("Oh no - {{bb:Mum}} has vanished too!"),
        _("Wait, there's another {{bb:note}}.\n"),
        _("Use {{yb:cat}} to {{lb:read}} the {{bb:note}}.")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = "cat note"
    hints = [_("{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}")]

    def next(self):
        return 10, 1
