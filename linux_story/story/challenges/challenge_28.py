#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
# from linux_story.story.challenges.challenge_29 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
import time


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
        "Let's {{lb:go into the restaurant}}."
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

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Look around {{lb:closely}}."
    ]

    start_dir = "~/town/east-part/restaurant"
    end_dir = "~/town/east-part/restaurant"

    hints = [
        "Eleanor: {{Bb:Do you remember how you found me?"
        " You used}} {{yb:ls -a}} {{Bb:right?}}"
    ]

    commands = [
        "ls -a"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "Do you see the .cellar?",
        "Let's {{lb:go in the .cellar}}."
    ]

    start_dir = "~/town/east-part/restaurant"
    end_dir = "~/town/east-part/restaurant/.cellar"

    hints = [
        "{{rb:Go in the wine cellar using}} {{yb:cd .cellar}}"
    ]

    commands = [
        "cd .cellar/",
        "cd .cellar"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    story = [
        "Look around."
    ]

    start_dir = "~/town/east-part/restaurant/.cellar"
    end_dir = "~/town/east-part/restaurant/.cellar"

    hints = [
        "{{rb:Look around with}} {{yb:ls}}"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateNano):
    story = [
        "You see a woman {{lb:Clara}} sitting in the cellar",
        "{{lb:Listen}} to what she has to say."
    ]

    start_dir = "~/town/east-part/restaurant/.cellar"
    end_dir = "~/town/east-part/restaurant/.cellar"

    hints = [
        "{{rb:Use}} {{lb:cat}} {{rb:to listen what she has to say.}}",
        "{{rb:Use}} {{yb:cat Clara}} {{rb:to listen to Clara.}}"
    ]

    commands = [
        "cat Clara"
    ]
    last_step = True

    def next(self):
        time.sleep(3)
        self.exit()
        # NextStep(self.xp)
