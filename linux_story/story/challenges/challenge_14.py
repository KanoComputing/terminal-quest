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
from linux_story.common import tq_file_system
from linux_story.story.challenges.challenge_15 import Step1 as NextStep
from linux_story.step_helper_functions import (
    unblock_commands_with_cd_hint, unblock_commands
)


class StepTemplateMv(TerminalMv):
    challenge_number = 14


class Step1(StepTemplateMv):
    story = [
        "{{lb:Guardiamo in giro}} per vedere che c'è "
        "da mangiare in cucina.\n"
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
		    "{{rb:Usa}} {{yb:ls}} {{rb:per guardare}} {{lb:intorno}} "
        "{{rb:in cucina.}}"
    ]

    def next(self):
        Step2()


# Move three pieces of food into the cestino
class Step2(StepTemplateMv):
    story = [
        "{{lb:Sposta}} tre cibi nel tuo cestino",
        "Puoi spostare più cose insieme usando {{lb:mv <una cosa> < altra cosa>"
        " <altra cosa ancora> cestino/}}.\n"
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    passable_items = [
        'banana',
        'torta',
        'cornetto',
        'tortina',
        'grappoli',
        'latte',
        'panino'
    ]
    unmovable_items = {
        "giornale": "{{rb:Hanno chiesto cibo, probabilmente "
        "non mangiano giornali.}}",

        "stufa": "{{rb:Sarà un po' pesa da trasportare, no?}}",

        "table": "{{rb:Sarà un po' pesa da trasportare, no?}}"
    }
    moved_items = []

    def block_command(self):
        separate_words = self.last_user_input.split(' ')

        if "cd" in self.last_user_input:
            return True

        if separate_words[0] == 'mv' and (separate_words[-1] == 'cestino' or
                                          separate_words[-1] == 'cestino/'):
            for item in separate_words[1:-1]:
                if item not in self.passable_items:
                    if item in self.unmovable_items:
                        self.send_hint(self.unmovable_items[item])
                        return True
                    else:
                        hint = (
                            "{{rb:Stai cercando di spostare qualcosa che "
                            "qui non c\'è.\nProva usando}} "
                            "{{yb:mv %s cestino/}}"
                            % self.passable_items[0]
                        )
                        self.send_hint(hint)
                        return True

            return False

    def check_command(self):

        separate_words = self.last_user_input.split(' ')
        all_items = []

        if self.get_command_blocked():
            hint = '{{rb:Prova usando}} {{yb:mv %s cestino/}}' \
                % self.passable_items[0]

        elif separate_words[0] == 'mv' and (separate_words[-1] == 'cestino' or
                                            separate_words[-1] == 'cestino/'):
            for item in separate_words[1:-1]:
                all_items.append(item)

            for item in all_items:
                self.passable_items.remove(item)

            hint = '\n{{gb:Ottimo!  continua così.}}'

        else:
            hint = '{{rb:Prova usando}} {{yb:mv %s cestino/}}' \
                % self.passable_items[0]

        self.send_hint(hint)

    # Check that the cestino folder contains the correct number of files?
    def check_output(self, output):
        cestino_dir = os.path.join(tq_file_system, 'casa-mia/cucina/cestino')
        food_files = [
            f for f in os.listdir(cestino_dir)
            if os.path.isfile(os.path.join(cestino_dir, f))
        ]

        if len(food_files) > 3:
            return True
        else:
            return False

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "\nOra bisogna tornare indietro nel {{bb:.riparo-nascosto}} con il "
        "cestino.",
        "{{lb:Sposta}} il {{lb:cestino}} di nuovo in {{lb:~}}.\n"
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = [
        "mv cestino ~",
        "mv cestino/ ~",
        "mv cestino ~/",
        "mv cestino/ ~/"
    ]
    hints = [
        "{{rb:Usa il comando}} {{yb:mv cestino ~/}} "
        "{{rb:per spostare il cestino nella strada ventosa ~}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "Torna nella strada con {{yb:cd}}.\n"
    ]
    start_dir = "~/casa-mia/cucina"
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
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Ora porta il cestino piena a quella famiglia.",
        "{{lb:Sposta}} il {{lb:cestino}} nel {{lb:paese/.riparo-nascosto}}.",
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
        "mv cestino paese/.riparo-nascosto",
        "mv cestino/ paese/.riparo-nascosto",
        "mv cestino paese/.riparo-nascosto/",
        "mv cestino/ paese/.riparo-nascosto/",
        "mv cestino ~/paese/.riparo-nascosto",
        "mv cestino/ ~/paese/.riparo-nascosto",
        "mv cestino ~/paese/.riparo-nascosto/",
        "mv cestino/ ~/paese/.riparo-nascosto/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:mv cestino paese/.riparo-nascosto/}} "
        "{{rb:per portare il cestino alla famiglia nascosta.}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step6()


class Step6(StepTemplateMv):
    story = [
        "{{gb:Ci siamo quasi!}} Ora {{lb:entra}} in "
        "{{lb:paese/.riparo-nascosto}} usando {{lb:cd}}.\n",
    ]

    start_dir = "~"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "cd paese/.riparo-nascosto",
        "cd paese/.riparo-nascosto/",
        "cd ~/paese/.riparo-nascosto",
        "cd ~/paese/.riparo-nascosto/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cd paese/.riparo-nascosto/}} "
        "{{rb:per riunirti con la famiglia nascosta.}}",
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        "{{wn:Controlla tutti con}} {{lb:cat}} {{wn:per vedere se "
        "sono contenti di poter mangiare.}}\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    hints = [
        "{{rb:Controlla tutti usando}} {{yb:cat}}"
    ]
    allowed_commands = {
        "cat Edith": (
            "\n{{wb:Edith:}} {{Bb:Hai salvato la mia bambina e il cane, "
            "e grazie a te ora non moriamo di fame...come ti posso "
            "ringraziare?}}\n"
        ),
        "cat Eleonora": (
            "\n{{wb:Eleonora:}} {{Bb:Evviva! Visto, te l'avevo detto Pippo, "
            "qualcuno ci avrebbe salvato.}}\n"
        ),
        "cat Edoardo": (
            "\n{{wb:Edoardo:}} {{Bb:Grazie!  Lo sapevo che l'avresti "
            "fatto per noi. Se veramente un eroe!}}\n"
        ),
        "cat cane": (
            "\n{{wb:Cane:}} {{Bb:\"Bau!\"}} {{wn:\nIl cane sembra parecchio "
            "eccitato.\n}}"
        )
    }

    last_step = True

    def check_command(self):
        if not self.allowed_commands:
            return True

        if self.last_user_input in self.allowed_commands.keys():

            hint = self.allowed_commands[self.last_user_input]
            del self.allowed_commands[self.last_user_input]
            num_people = len(self.allowed_commands.keys())

            if num_people == 0:
                hint += '\n{{gb:Premi Invio per continuare.}}'

            # If the hint is not empty
            elif hint:
                if num_people > 1:
                    hint += (
                        "\n{{gb:Controllane altri}} {{yb:" + str(num_people) +
                        "}} {{gb:.}}"
                    )
                else:
                    hint += (
                        "\n{{gb:Controllane un altro}}"
                    )
        else:
            hint = (
                "{{rb:Usa}} {{yb:" + self.allowed_commands.keys()[0] +
                "}} {{rb:per andare avanti.}}"
            )

        self.send_hint(hint)

    def next(self):
        sys.exit("LAVORI IN CORSO! Traduzione in italiano arrivata fino a qui (25 settembre 2015)\n")
        #arf NextStep(self.xp)
