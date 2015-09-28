#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_14 import Step1 as NextStep
from linux_story.step_helper_functions import (
    unblock_commands_with_cd_hint, unblock_commands
)


class StepTemplateMv(TerminalMv):
    challenge_number = 13


class Step1(StepTemplateMv):
    story = [
        "{{wb:Edoardo:}} {{Bb:\"Grazie grazie per aver salvato la mia bambina!",
        "Ma avrei da chiedere un altro favore...",

        "Non abbiamo niente da mangiare. Ci potresti portare qualcosa? "
        "Non abbiamo avuto tempo di prendere nulla quando ci siamo nascosti.\"",

        "\"Ti ricordi di avere visto cibo recentemente?\"}}",

        "\n...ah! tutto quel cibo nella tua {{bb:cucina}}! "
        "Potremmo dare qualcosa a questa famiglia.",

        "\nCominciamo a {{lb:spostare}} il {{lb:cestino}} in {{lb:~}}. "
        "Usa il comando {{yb:mv cestino ~/}}\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "mv cestino ~",
        "mv cestino/ ~",
        "mv cestino ~/",
        "mv cestino/ ~/",
        "mv cestino ../..",
        "mv cestino/ ../..",
        "mv cestino ../../",
        "mv cestino/ ../../"
    ]
    hints = [
        "{{rb:Usa il comando}} {{yb:mv cestino ~/}} "
        "{{rb:per spostare}} {{lb:il cestino}} {{rb:to sulla strada ventos}} {{lb:~}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "Ora segui il cestino. Usa {{yb:cd}} da solo "
        "per {{lb:andare}} nella strada ventosa ~.\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~"
    commands = [
        "cd",
        "cd ~",
        "cd ~/"
    ]
    hints = [
        "{{rb:Usa il comando}} {{yb:cd}} {{rb:da solo "
        "per spostarti sulla strada ~}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "Ora sei di nuovo sulla lunga strada ventosa . {{lb:Guarda in giro}} "
        "con {{yb:ls}} per vedere se hai il cestino con te.\n"
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
        "ls"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:da solo "
        "per guardare in giro.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "Tieni ben stretto il cestino, e "
        "intanto ti avvicini a {{bb:casa-mia}}.",
        "Sposta il {{lb:cestino}} in {{lb:casa-mia/cucina}}.",
        "Non dimenticare di usare il tasto TAB per finire prima di scrivere i comandi.\n"
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
        "mv cestino casa-mia/cucina",
        "mv cestino/ casa-mia/cucina",
        "mv cestino casa-mia/cucina/",
        "mv cestino/ casa-mia/cucina/",
        "mv cestino ~/casa-mia/cucina",
        "mv cestino/ ~/casa-mia/cucina",
        "mv cestino ~/casa-mia/cucina/",
        "mv cestino/ ~/casa-mia/cucina/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:mv cestino casa-mia/cucina/}} "
        "{{rb:per spostare il cestino nella tua cucina.}}",
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Ora {{lb:vai}} in {{lb:casa-mia/cucina}} usando {{lb:cd}}.\n",
    ]

    start_dir = "~"
    end_dir = "~/casa-mia/cucina"
    commands = [
        "cd casa-mia/cucina",
        "cd casa-mia/cucina/",
        "cd ~/casa-mia/cucina",
        "cd ~/casa-mia/cucina/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cd casa-mia/cucina/}} "
        "{{rb:per andare nella tua cucina.}}",
    ]
    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextStep(self.xp)
