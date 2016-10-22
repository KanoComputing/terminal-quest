#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.challenges.challenge_41 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 40


# Note reads:
# We need to find a special command which makes the User into a Super User.
# I'm down the rabbithole. Don't worry, there are no nasty surprises here.
class Step1(StepTemplateChmod):
    story = [
        "..no nasty surprises, ok that's good. Let's go inside the rabbithole."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{rb:Use}} {{yb:cd rabbithole/}} {{rb:to go inside.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Look around"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "You see a Rabbit, a piece of paper and a doorway.",
        "This Rabbit looks somewhat familiar...",
        "{{lb:Listen}} to the Rabbit."
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "cat Rabbit"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat Rabbit}} {{rb:to examine the Rabbit.}}"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = [
        "Rabbit: {{Bb:...}}",
        "It seems the Rabbit doesn't say very much. That's quite normal for "
        "rabbits.",
        "Let's read the {{lb:note}}."
    ]
    start_dir = "~/woods/thicket/.rabbithole"
    end_dir = "~/woods/thicket/.rabbithole"
    commands = [
        "cat note"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}"
    ]

    def next(self):
        NextStep(self.xp)
