#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU Gpl v2
#
# A chapter of the story

#arf This just for the momentaneous interruption
import sys

from linux_story.step_helper_functions import (
    unblock_commands_with_mkdir_hint, unblock_cd_commands
)
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_21 import Step1 as NextStep


class StepTemplateEcho(TerminalEcho):
    challenge_number = 20


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 20


class Step1(StepTemplateEcho):
    print_text = [
        "{{yb:\"Qualcuno è sopravissuto nascondendosi.\"}}"
    ]
    story = [
        "Romina: {{Bb:Oh! Questo mi ricorda che mio marito aveva l'abitudine "
        "di costruire dei ripari speciali per proteggere le piante in inverno. "
        "Credo che utilizzasse un attrezzo specifico. "
        "Dovremmo cercare nel suo capanno degli attrezzi per trovarlo.}}",
        "\nUsa il comando {{lb:cd}} per andare nel capanno degli attrezzi.\n"
    ]

    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/capanno-degli-attrezzi"
    hints = [
        "{{rb:Vai nel capanno degli attrezzi al volo"
        " usando}} {{yb:cd ../capanno-degli-attrezzi/}}"
    ]

    path_hints = {
        "~/fattoria/fienile": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ../}} {{rb:per tornare indietro.}}"
        },
        "~/fattoria": {
            "not_blocked": "\n{{gb:Ottimo! Ora vai nel}} {{lb:capanno-degli-attrezzi}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd capanno-degli-attrezzi/}} {{rb:per andare nel capanno-degli-attrezzi.}}"
        }
    }

    def check_command(self):
        if self.current_path == self.end_dir:
            return True
        elif "cd" in self.last_user_input and not self.get_command_blocked():
            hint = self.path_hints[self.current_path]["not_blocked"]
        else:
            hint = self.path_hints[self.current_path]["blocked"]

        self.send_text(hint)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateEcho):
    story = [
        "Romina ti segue nel {{bb:capanno-degli-attrezzi}}. È uno spazio "
        "molto grande con attrezzi di ogni tipo appoggiati alle pareti.",
        "Romina: {{Bb:Vediamo di}} {{lb:cercare attorno}} {{Bb:per "
        "trovare qualcosa di utile.}}\n"
    ]
    start_dir = "~/fattoria/capanno-degli-attrezzi"
    end_dir = "~/fattoria/capanno-degli-attrezzi"
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per cercare attorno.}}"
    ]
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./",
        "ls -a .",
        "ls -a ./"
    ]
    # Move Romina into capanno-degli-attrezzi
    story_dict = {
        "Romina": {
            "path": "~/fattoria/capanno-degli-attrezzi"
        }
    }
    deleted_items = ["~/fattoria/fienile/Romina"]

    def next(self):
        Step3()


class Step3(StepTemplateEcho):
    story = [
        "Romina: {{Bb:Ah, guarda! C'è un foglio, ci sono delle istruzioni "
        "sotto}} {{lb:MKDIR}}{{Bb:.}}",
        "{{Bb:Che dicono?}}",
        "\n{{lb:Leggi}} le istruzioni intitolate {{lb:MKDIR}}."
    ]
    hints = [
        "Romina: {{Bb:\"...sai leggere, vero? Usa}} {{lb:cat}} "
        "{{Bb:per leggere le cose.\"}}",
        "Romina: {{Bb:\"Che è quello che voi bambini imparate a scuola oggigiorno...\""
        "\n\"Usa semplicemente}} {{yb:cat MKDIR}} {{Bb:per legger eil foglio.\"}}",
        "{{rb:Usa}} {{yb:cat MKDIR}} {{rb:per leggerlo.}}"
    ]
    start_dir = "~/fattoria/capanno-degli-attrezzi"
    end_dir = "~/fattoria/capanno-degli-attrezzi"
    commands = "cat MKDIR"

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Romina: {{Bb:Questo dice che puoi fare qualcosa con qualcosa "
        "che si chiama}} {{lb:mkdir}}{{Bb:?}}",
        "\n{{gb:Prova a fare un igloo usando}} {{yb:mkdir igloo}}"
    ]
    hints = [
        "{{rb:Crea la struttura di un igloo usando}} {{yb:mkdir igloo}}\n"
    ]
    start_dir = "~/fattoria/capanno-degli-attrezzi"
    end_dir = "~/fattoria/capanno-degli-attrezzi"
    commands = [
        "mkdir igloo"
    ]

    def block_command(self):
        return unblock_commands_with_mkdir_hint(
            self.last_user_input, self.commands
        )

    def check_command(self):
        if self.last_user_input == "cat MKDIR":
            self.send_hint("\n{{gb:Hai fatto bene a ricontrollare la pagina!}}")
            return False

        return StepTemplateMkdir.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Ora {{lb:guarda attorno}} per vedere se è cambiato qualcosa."
    ]
    start_dir = "~/fattoria/capanno-degli-attrezzi"
    end_dir = "~/fattoria/capanno-degli-attrezzi"
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./"
    ]
    hints = [
        "{{rb:guarda attorno usando}} {{yb:ls}}{{rb:.}}"
    ]
    last_step = True

    def next(self):
        sys.exit("LAVORI IN CORSO! Traduzione in italiano arrivata fino a qui (25 settembre 2015)\n")
        NextStep(self.xp)
