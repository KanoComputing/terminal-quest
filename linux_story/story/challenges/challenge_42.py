#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.challenges.challenge_43 import Step1 as NextStep


# Note reads:
# We need to find a special command which makes the User into a Super User.
# I'm down the rabbithole. Don't worry, there are no nasty surprises here.
# class Step1(StepTemplateChmod):
#     story = [
#         "..no nasty surprises, ok that's good. Let's go inside the rabbithole."
#     ]
#     start_dir = "~/woods/thicket"
#     end_dir = "~/woods/thicket/rabbithole"
#     hints = [
#         "{{rb:Use}} {{yb:cd rabbithole/}} {{rb:to go inside.}}"
#     ]
#
#     def block_command(self):
#         return unblock_cd_commands(self.last_user_input)
#
#     def next(self):
#         Step2()
#
#
# class Step2(StepTemplateChmod):
#     story = [
#         "Look around"
#     ]
#     start_dir = "~/woods/thicket/rabbithole"
#     end_dir = "~/woods/thicket/rabbithole"
#     commands = [
#         "ls",
#         "ls -a"
#     ]
#     hints = [
#         "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
#     ]
#
#     def next(self):
#         Step4()
#
#
# class Step4(StepTemplateChmod):
#     story = [
#         "You see a Rabbit, a piece of paper and a doorway.",
#         "This Rabbit looks somewhat familiar...",
#         "{{lb:Listen}} to the Rabbit."
#     ]
#     start_dir = "~/woods/thicket/rabbithole"
#     end_dir = "~/woods/thicket/rabbithole"
#     commands = [
#         "cat Rabbit"
#     ]
#     hints = [
#         "{{rb:Use}} {{yb:cat Rabbit}} {{rb:to examine the Rabbit.}}"
#     ]
#
#     def next(self):
#         Step5()


GO_TO_THE_LIBRARY = [
    "The Rabbit wants to know where the Super User command is kept?",
    "....",
    "Where could that be?",
    ""
    # "Let's head there. It looks as if the Rabbit will follow."
]

RABBITS_ARE_QUIET = [
    "Rabbit: {{Bb:...}}",
    "",
    "It seems the Rabbit doesn't say very much. That's quite normal for rabbits."
]


class TerminalRabbit(TerminalChmod):
    rabbit_text = "The rabbit is in front of the rabbithole and won't let you pass"

    def block_command(self):
        if "rabbithole" in self.last_user_input and \
                (
                    "ls" in self.last_user_input or
                    "cat" in self.last_user_input
                ):
            print self.rabbit_text
            return True
        else:
            return TerminalChmod.block_command(self)

    def autocomplete_files(self, text, line, begidx, endidx, only_dirs=False,
                           only_exe=False):
        completions = TerminalChmod.autocomplete_files(
            self, text, line, begidx, endidx, only_dirs,
            only_exe
        )
        if "cage/" in completions or "Mum" in completions:
            print "\n" + self.rabbit_text
            return []
        else:
            return completions


class StepTemplateChmod(TerminalRabbit):
    challenge_number = 42


# Same as the towns people, and the last challenge?
class Step1(StepTemplateChmod):
    story = [
        "You see a Rabbit, a piece of paper and a doorway.",
        "This Rabbit looks somewhat familiar...",
        "{{lb:Listen}} to the Rabbit."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    hints = [
        "{{rb:Use}} {{yb:cat Rabbit}} {{rb:to examine the Rabbit.}}"
    ]

    commands_done = {
        "cat note":  False,
        "cat Rabbit": False
    }

    def check_command(self):
        if self.last_user_input == "cat note":
            self.commands_done[self.last_user_input] = True
            # self.send_hint("\nThe Rabbit wants to know where the Super User command is kept...")

        if self.last_user_input == "cat Rabbit":
            return True

        return False

    def next(self):
        if self.commands_done["cat note"]:
            Step4()
        else:
            Step2()


class Step2(StepTemplateChmod):
    story = RABBITS_ARE_QUIET + ["", "{{lb:Examine}} the note."]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    commands = [
        "cat note"
    ]

    def next(self):
        Step3(self.xp)


class Step3(StepTemplateChmod):
    story = GO_TO_THE_LIBRARY
    start_dir = "~/woods/thicket"
    end_dir = "~/town/east/library"
    hints = [
        "{{rb:Use}} {{yb:cd ~/town/east/library}} {{rb:to go to the library}}"
    ]
    last_step = True

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)


class Step4(StepTemplateChmod):
    story = RABBITS_ARE_QUIET + [""] + GO_TO_THE_LIBRARY
    start_dir = "~/woods/thicket"
    end_dir = "~/town/east/library"
    hints = [
        "{{rb:Is this the same place the swordsmaster referred to?}}"
        "{{rb:Use}} {{yb:cd ~/town/east/library}} {{rb:to go to the library}}"
    ]
    last_step = True

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)
