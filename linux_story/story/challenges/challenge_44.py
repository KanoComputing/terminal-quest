#!/usr/bin/env python
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
import time
from linux_story.story.terminals.terminal_sudo import TerminalSudo
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateSudo(TerminalSudo):
    challenge_number = 44



class Step1(StepTemplateSudo):
    story = [
        "The command locked away has been stolen...",
        "...",
        "What should you do now?",
    ]

    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    def next(self):
        Step2()


class Step2(StepTemplateSudo):
    story = [
        "The swordmaster appears.",
        "Swordsmaster: {{Bb:I felt something shift...did you get the command?}}",
        "",
        "{{yb:1: A white rabbit stole the command.}}",
        "{{yb:2: Yeah I got it. Nothing else happened.}}",
        "{{yb:3: Please don't kill me.}}"
    ]

    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    extra_hints = {
        "echo 2": "Swordsmaster: {{Bb:...tell me the truth. What happened here?}}",
        "echo 3": "Swordsmaster: {{Bb:..I can't promise that.}}"
    }
    commands = [
        "echo 1"
    ]

    def check_command(self):
        if self.last_user_input in self.extra_hints:
            self.send_hint(self.extra_hints[self.last_user_input])

        return StepTemplateSudo.check_command(self)

    def next(self):
        Step3()


class Step3(StepTemplateSudo):
    story = [
        "Swordsmaster: {{Bb:A white rabbit? An old friend of mine, the Judoka, used to have a white rabbit...}}",
        "{{Bb:Tell me, was there anything unusual about this rabbit?}}"
        "",
        "{{yb:1: It communicated via notes.}}",
        "{{yb:2: I think I've seen it before.}}",
        "{{yb:3: It was carrying something.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    extra_hints = {
        "echo 2": "Swordsmaster: {{Bb:It could have been watching you for a while. Was there anything else?}}",
        "echo 1": "Swordsmaster: {{Bb:Well rabbits can't normally speak. How else did you expect it to communicate?}}"
    }
    commands = [
        "echo 3"
    ]

    def check_command(self):
        if self.last_user_input in self.extra_hints:
            self.send_hint(self.extra_hints[self.last_user_input])

        return StepTemplateSudo.check_command(self)

    def next(self):
        Step4()


class Step4(StepTemplateSudo):
    story = [
        "Swordsmaster: {{Bb:Could this be the bell you've been hearing that makes people disappear?}}",
        "{{Bb:I wonder if this is controlling the rabbit in some way...}}",
        "{{Bb:I want to find the Judoka and see if he has a solution to this.}}"
    ]


class Step5(StepTemplateSudo):
    story = [
        "Swordsmaster: {{Bb:It's not all over yet. To use the}} {{lb:command you picked up}} {{Bb:you need to know "
        "the password.}}",
        "{{Bb:If the rabbit doesn't know the password, then we have some time. I need you to try and guess it.}}",
        "{{Bb:Use}} {{yb:sudo ls}} {{Bb:to look around.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    hints = [
        "Swordsmaster: {{Bb:Use}} {{yb:sudo ls}} {{to look around.}}"
    ]
    commands = [
        "sudo ls"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateSudo):
    story = [
        "{{Bb:I need you to face the rabbit, and do whatever you have to to stop this.}}",
        "{{Bb:I will teach you the command to remove this...creature, should the worst come to that}}",
        "{{Bb:Take a look at my sword.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    hints = [
        "Swordsmaster: {{Bb:Examine my sword with}} {{yb:cat sword}}"
    ]
    commands = [
        "cat sword"
    ]

    def next(self):
        pass

