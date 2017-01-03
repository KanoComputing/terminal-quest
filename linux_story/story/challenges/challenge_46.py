#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.Animation import Animation
from linux_story.StepTemplate import StepTemplate
from linux_story.story.terminals.terminal_rm import TerminalRm


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm


class Step1(StepTemplateRm):
    story = [
        _("{{gb:You saved all the villagers.}}"),
        _("You are alone with the Rabbit and the bell."),
        "",
        _("Time to end this.")
    ]

    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "rm bell"
    ]
    hints = [
        _("{{rb:Use}} {{yb:rm bell}} {{rb:to remove the bell.}}")
    ]
    dark_theme = True


    def block_command(self, line):
        if line == "rm Rabbit":
            print _("The rabbit dodged the attack!")
            return True
        return StepTemplateRm.block_command(self, line)

    def check_command(self, line):
        if self.get_last_user_input() == "rm Rabbit":
            self.send_hint(
                _("{{lb:The rabbit dodged the attack!}} {{rb:Remove the bell with}} {{yb:rm bell}}")
            )
            return

        return StepTemplateRm.check_command(self, line)

    def next(self):
        Animation("gong-being-removed").play_finite(1)
        self.send_normal_theme()
        Animation("rabbit-blinking").play_finite(1)
        return 46, 2


class Step2(StepTemplateRm):
    story = [
        _("The anger behind the rabbit's eyes fades, and is replaced with confusion."),
        "",
        _("The swordmaster runs into the room."),
        "",
        _("Swordmaster: {{Bb:You did it! The rabbit is free of the cursed bell, and you've saved everyone who was "
        "kidnapped.}}"),
        "",
        _("{{Bb:The chest the Rabbit stole is right here. Have you gone through the contents?}}"),
        "",
        _("{{lb:Examine the contents of the chest.}}")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "cat chest/torn-scroll"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat chest/torn-scroll}} {{rb:to examine the contents.}}")
    ]

    def check_command(self, line):
        if line == "cat chest/torn-note":
            return False
        return StepTemplateRm.check_command(self, line)

    def next(self):
        return 46, 3


class Step3(StepTemplateRm):
    story = [
        _("The Rabbit sniffs around the chest."),
        _("It doesn't seem to recognise it."),
        "",
        _("Swordmaster: {{Bb:It looks as though the command was torn in half.}}"),
        _("{{Bb:Maybe the rabbit hid it when it was possessed. It doesn't look like it remembers.}}"),
        _("{{Bb:The command could be anywhere. Who knows where it is hidden....}}")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"

    def next(self):
        self._is_finished = True
        self.exit()
        return -1, -1
