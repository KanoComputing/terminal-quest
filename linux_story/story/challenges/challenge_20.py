#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU Gpl v2
#
# A chapter of the story

from linux_story.step_helper_functions import (
    unblock_commands_with_cd_hint, unblock_commands_with_mkdir_hint
)
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_21 import Step1 as NextStep


class StepTemplateEcho(TerminalEcho):
    challenge_number = 20


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 20


class Step1(StepTemplateEcho):
    print_text = [
        "{{yb:\"Some people survived by going into hiding.\"}}"
    ]
    story = [
        "Ruth: {{Bb:Oh! That reminds me, my husband used "
        "to build special shelters to store crops in over winter. "
        "I think he used a specific tool. "
        "We should take a look in his toolshed to see if we can find it.}}",
        "\nUse the {{lb:cd}} command to go into the toolshed.\n"
    ]

    commands = [
        "cd ../toolshed",
        "cd ../toolshed/"
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/toolshed"
    hints = [
        "{{rb:Go to the toolshed in one step"
        " using}} {{yb:cd ../toolshed/}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step2()


class Step2(StepTemplateEcho):
    story = [
        "Ruth follows you into the toolshed. It's a very large "
        "space with tools lining the walls.",
        "Ruth: {{Bb:Let's}} {{lb:look around}} {{Bb:for "
        "anything that could be useful.}}\n"
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./",
        "ls -a .",
        "ls -a ./"
    ]
    # Move Ruth into toolshed
    story_dict = {
        "Ruth": {
            "path": "~/farm/toolshed"
        }
    }
    deleted_items = ["~/farm/barn/Ruth"]

    def next(self):
        Step3()


class Step3(StepTemplateEcho):
    story = [
        "Ruth: {{Bb:Ah, look! There are some instructions "
        "under}} {{lb:MKDIR}}{{Bb:.}}",
        "{{Bb:What does it say?}}",
        "\n{{lb:Examine}} the {{lb:MKDIR}} instructions."
    ]
    hints = [
        "Ruth: {{Bb:\"...you are able to read, yes? You use}} {{lb:cat}} "
        "{{Bb:to read things.\"}}",
        "Ruth: {{Bb:\"What do you kids learn in schools nowadays...\""
        "\n\"Just use}} {{yb:cat MKDIR}} {{Bb:to read the paper.\"}}",
        "{{rb:Use}} {{yb:cat MKDIR}} {{rb:to read it.}}"
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    commands = "cat MKDIR"

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:This says you can make something using something "
        "called}} {{lb:mkdir}}{{Bb:?}}",
        "\n{{gb:Try making an igloo using}} {{yb:mkdir igloo}}"
    ]
    hints = [
        "{{rb:Create an igloo structure by using}} {{yb:mkdir igloo}}\n"
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    commands = "mkdir igloo"

    def block_command(self):
        return unblock_commands_with_mkdir_hint(
            self.last_user_input, self.commands
        )

    def check_command(self, current_dir):
        if self.last_user_input == "cat MKDIR":
            self.send_hint("\n{{gb:Well done for checking the page again!}}")
            return False

        return StepTemplateMkdir.check_command(self, current_dir)

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Now have a {{lb:look around}} and see what's changed."
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./"
    ]
    hints = [
        "{{rb:Look around using}} {{yb:ls}}{{rb:.}}"
    ]

    def next(self):
        NextStep(self.xp)
