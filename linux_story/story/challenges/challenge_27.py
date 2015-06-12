#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.terminals.terminal_nano import TerminalNano
# from linux_story.story.challenges.challenge_28 import Step1 as NextChallengeStep


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 27


class StepTemplateNano(TerminalNano):
    challenge_number = 27


class Step1(StepTemplateMkdir):
    story = [
        "You are back in the shed-maker's place.",
        "Have a look around."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    commands = [
        "ls",
        "ls -a"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Bernard: {{Bb:Hellooooo. You came back to fix my script!}}",

        "Let's see whether we can fix it.",

        "Let's try and use {{yb:nano best-horn-in-the-world.sh}} to "
        "edit it."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    commands = [
        "nano best-horn-in-the-world.sh"
    ]

    hints = [
        "{{rb:Use}} {{yb:nano best-horn-in-the-world}} "
        "{{rb:to edit the tool.}}"
    ]

    nano_end_content = "echo \"Honk!\""
    goal_nano_filepath = "~/town/east-part/shed-shop/best-horn-in-the-world.sh"
    goal_nano_save_name = "best-horn-in-the-world.sh"

    # Overwrite the default behaviour for most of the steps - nano needs
    # slightly different behaviour.
    def check_command(self, current_dir):
        return self.check_nano_input()

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Now time to test your script!",
        "Use {{yb:./best-horn-in-the-world.sh}} to run it."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    commands = [
        "./best-horn-in-the-world.sh"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "{{gb:Congratulations, the script now prints \"Honk!\"}}",
        "\nBernard: {{Bb:The tool is working! Wonderful! "
        "Thank you so much!}}",
        "It occurs to you that we haven't asked Bernard much about himself.",
        "What would you like to ask him?",
        "{{yb:1: \"Are you going into hiding now?\"",
        "2: \"What's the next big tool you want to create?\"",
        "3: \"What's in the secret room?\"}}",
        "\nUse {{lb:echo}} to ask him a question."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]

    def next(self):
        pass
