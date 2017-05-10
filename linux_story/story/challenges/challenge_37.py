#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.PlayerLocation import generate_real_path
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file
from linux_story.helper_functions import has_write_permissions, has_read_permissions, has_execute_permissions
from linux_story.story.terminals.terminal_chmod import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        _("You set off the firework!"),
        _("{{gb:You learnt all the chmod commands.}}"),
        "",
        _("{{lb:Thunk.}}"),
        "",
        _("Something new landed in front of you."),
        _("{{lb:Look around}} to see what it is.")
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
        _("{{rb:Use}} {{yb:ls}} {{rb:to see what landed in front of you.}}")
    ]
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        return 37, 2


class Step2(StepTemplateChmod):
    story = [
        _("There is a {{bb:chest}} in front of you."),
        _("It is wrapped tightly by a big chain."),
        _("{{lb:Look inside the chest.}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    hints = [
        _("{{rb:Use}} {{yb:ls chest}} {{rb:to see inside the chest.}}")
    ]
    commands = [
        "ls chest",
        "ls chest/"
    ]

    def next(self):
        return 37, 3


class Step3(StepTemplateChmod):
    story = [
        _("The chain won't budge. You cannot see inside, nor access its contents."),
        "",
        _("Break the chain."),
        _("{{lb:You'll need to combine all the chmod flags you've just learnt.}}")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    hints = [
        "{{lb:r, w and x}} {{rb:were the flags.}}",
        "{{rb:Use}} {{yb:chmod +rwx chest}} {{rb:to unlock the chest.}}"
    ]

    def check_command(self, line):
        chest = generate_real_path("~/woods/cave/chest")
        if has_write_permissions(chest) and has_read_permissions(chest) and has_execute_permissions(chest):
            return True
        self.send_stored_hint()

    def next(self):
        return 37, 4


class Step4(StepTemplateChmod):
    story = [
        _("{{gb:You opened it!}}"),
        _("Now {{lb:look inside}} the chest.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"

    commands = [
        "ls chest",
        "ls chest/"
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls chest/}} {{rb:to look inside the chest.}}")
    ]

    def next(self):
        return 37, 5


class Step5(StepTemplateChmod):
    story = [
        _("You see a riddle, and an answer. {{lb:Examine}} them.")
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat chest/answer"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat chest/answer}} {{rb:to examine the answer in the chest.}}")
    ]

    def check_command(self, last_user_input):
        if last_user_input == "cat chest/riddle":
            self.send_hint(
                _("{{gb:That looks like the riddle the swordmaster asked you.}}")
            )
            return
        return StepTemplateChmod.check_command(self, last_user_input)

    def next(self):
        return 38, 1
