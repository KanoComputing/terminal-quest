#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.challenges.challenge_32 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 31


class Step1(StepTemplateNano):
    story = [
        "You've arrived in the shed-shop. {{lb:Look around.}}"
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Huh, you can't see Bernard anywhere.",

        "I wonder where he went.",

        "Maybe he's in his {{lb:basement}}? Let's {{lb:go}} inside."
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop/basement"
    hints = [
        "{{rb:Go into the basement with}} {{yb:cd basement/}}"
    ]

    def check_command(self):
        if self.last_user_input == "cat bernards-hat":
            self.send_text(
                "\nIs that Bernard\'s hat? "
                "Strange he left it behind..."
            )
        else:
            return TerminalNano.check_command(self)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "You walked into Bernard's basement. {{lb:Look around.}}"
    ]
    start_dir = "~/town/east/shed-shop/basement"
    end_dir = "~/town/east/shed-shop/basement"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Look around with}} {{yb:ls}}{{rb:.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "You see what looks like another tool and a couple of diaries.",
        "{{lb:Examine}} them."
    ]
    start_dir = "~/town/east/shed-shop/basement"
    end_dir = "~/town/east/shed-shop/basement"
    commands = [
        "cat bernards-diary-1",
        "cat bernards-diary-2",
        "cat photocopier.sh"
    ]
    hints = [
        "{{rb:Use}} {{lb:cat}} {{rb:to examine the objects around you.}}"
    ]

    def check_command(self):
        if self.last_user_input in self.commands:
            self.commands.remove(self.last_user_input)

            if not self.commands:
                text = (
                    "\n{{gb:Press Enter to continue.}}"
                )
                self.send_text(text)

            else:
                text = (
                    "\n{{gb:Well done! Look at the other objects.}}"
                )
                self.send_text(text)

        elif not self.last_user_input and not self.commands:
            return True

        else:
            return StepTemplateNano.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    story = [
        "Enough wandering. Let's go and try and find the "
        "{{lb:masked swordsmaster}} near the woods, and see "
        "what information he can tell us.",
        "\n{{gb:Press Enter to continue.}}"
    ]
    start_dir = "~/town/east/shed-shop/basement"
    end_dir = "~/town/east/shed-shop/basement"
    # last_step = True

    # Add all the new files here.

    def next(self):
        NextStep(self.xp)
