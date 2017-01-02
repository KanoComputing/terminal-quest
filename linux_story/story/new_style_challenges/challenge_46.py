#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.Animation import Animation
from linux_story.IStep import IStep
from linux_story.story.new_terminals.terminal_rm import TerminalRm


class StepTemplateRm(IStep):
    TerminalClass = TerminalRm


class Step1(StepTemplateRm):
    story = [
        "{{gb:You saved all the villagers.}}",
        "You are alone with the Rabbit and the bell.",
        "",
        "Time to end this."
    ]

    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "rm bell"
    ]
    hints = [
        "{{rb:Use}} {{yb:rm bell}} {{rb:to remove the bell.}}"
    ]
    dark_theme = True


    def block_command(self, line):
        if line == "rm Rabbit":
            print "The rabbit dodged the attack!"
            return True
        return StepTemplateRm.block_command(self, line)

    def check_command(self, line):
        if self.get_last_user_input() == "rm Rabbit":
            self.send_hint("{{lb:The rabbit dodged the attack!}} {{rb:Remove the bell with}} {{yb:rm bell}}")
            return

        return StepTemplateRm.check_command(self, line)

    def next(self):
        Animation("gong-being-removed").play_finite(1)
        self.send_normal_theme()
        Animation("rabbit-blinking").play_finite(1)
        return 46, 2


class Step2(StepTemplateRm):
    story = [
        "The anger behind the rabbit's eyes fades, and is replaced with confusion.",
        "",
        "The swordmaster runs into the room.",
        "",
        "Swordmaster: {{Bb:You did it! The rabbit is free of the cursed bell, and you've saved everyone who was "
        "kidnapped.}}",
        "",
        "{{Bb:The chest the Rabbit stole is right here. Have you gone through the contents?}}",
        "",
        "{{lb:Examine the contents of the chest.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "cat chest/torn-scroll"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat chest/torn-scroll}} {{rb:to examine the contents.}}"
    ]

    def check_command(self, line):
        if line == "cat chest/torn-note":
            return False
        return StepTemplateRm.check_command(self, line)

    def next(self):
        return 46, 3


class Step3(StepTemplateRm):
    story = [
        "The Rabbit sniffs around the chest.",
        "It doesn't seem to recognise it.",
        "",
        "Swordmaster: {{Bb:It looks as though the command was torn in half.}}",
        "{{Bb:Maybe the rabbit hid it when it was possessed. It doesn't look like it remembers.}}",
        "{{Bb:The command could be anywhere. Who knows where it is hidden....}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"

    def next(self):
        self._is_finished = True
