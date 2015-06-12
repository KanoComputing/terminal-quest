#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
# from linux_story.story.challenges.challenge_29 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 28


class Step1(StepTemplateNano):
    story = [
        "Where could the librarian be hiding?",
        "{{lb:Look around}} to decide where to go next."
    ]

    start_dir = "~/town/east-part"
    end_dir = "~/town/east-part"

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
        "We haven't checked out the restaurant yet.",
        "Let's {[lb:go into the restaurant}}."
    ]

    start_dir = "~/town/east-part"
    end_dir = "~/town/east-part/restaurant"

    hints = [
        "{{rb:Use}} {{yb:cd restaurant}} {{rb:to look in the restaurant}}"
    ]
    commands = [
        "cd restaurant/",
        "cd restaurant"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Look around {{lb:closely}}."
    ]

    start_dir = "~/town/east-part/restaurant"
    end_dir = "~/town/east-part/restaurant"

    hints = [
        "{{rb:Look around}} {{lb:closely}}",

        "Eleanor: {{Bb:Do you remember how to look around?"
        "You use}} {{lb:ls}} {{Bb:right?}}"
    ]

    commands = [
        "ls -a"
    ]

    def check_command(self, current_dir):
        if self.last_user_input == "ls":
            text = (
                "\nYou need to look around more closely "
                "with {{yb:ls -a}}"
            )
            self.send_text(text)
            return False
        else:
            StepTemplateNano.check_command(self, current_dir)


class Step4(StepTemplateNano):

