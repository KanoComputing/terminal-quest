#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_25 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 24


class Step1(StepTemplateMkdir):
    story = [
        "Look around."
    ]
    commands = [
        "ls",
        "ls -a"
    ]

    start_dir = "~/town/east-part"
    end_dir = "~/town/east-part"
    hints = [
        "{{rb:Look around with}} {{yb:ls}}{{rb:.}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Eleanor: {{Bb:Hey, what is that shed-shop?}}",
        "{{Bb:Let's}} {{lb:go in}}{{Bb:!}}"
    ]

    start_dir = "~/town/east-part"
    end_dir = "~/town/east-part/shed-shop"
    commands = [
        "cd shed-shop",
        "cd shed-shop/"
    ]
    hints = [
        "{{rb:Use}} {{yb:cd shed-shop/}} {{rb:to go in the shed-shop.}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step3()


# Duplicate of Step1, except that self.next is changed
class Step3(StepTemplateMkdir):
    # Have a sign with "the-best-shed-maker-in-town"

    story = [
        "Look around."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"
    hints = [
        "{{rb:Look around with}} {{yb:ls}}{{rb:.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):

    story = [
        "You see a man called Bernard, a door and a "
        "couple of tools.",
        "\nThe tools show up as {{gb:green}} in the Terminal.",
        "\n{{lb:Listen}} to what {{lb:Bernard}} has to say."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    hints = [
        "Eleanor: {{Bb:My}} {{lb:cat}} {{Bb:used to be a great "
        "listener, I'd tell her everything.}}",
        "{{rb:Use}} {{yb:cat Bernard}} {{rb:to see what Bernard has "
        "to say.}}"
    ]

    commands = [
        "cat Bernard"
    ]

    last_step = True

    def next(self):
        NextStep(self.xp)
