#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

#arf Just for the momentaneous interruption
import sys

from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.terminals.terminal_eleanor import TerminalMkdirEleanor
from linux_story.story.challenges.challenge_24 import Step1 as NextStep


class StepMkdir(TerminalMkdir):
    challenge_number = 23


class StepMkdirEleanor(TerminalMkdirEleanor):
    challenge_number = 23


class Step1(StepMkdir):
    story = [
        "Ecco Eleonora. Sentiamo cos'ha da raccontare."
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "cat Eleonora"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat Eleonora}} {{rb:per sapere cos'ha da raccontare.}}"
    ]

    def next(self):
        Step2()


class Step2(StepMkdir):
    story = [
        "Eleonora: {{Bb:\"Ah, sei te!",
        # "My parents went outside as we ran out of food."
        "Hai visto la mia mamma e il mio babbo?\"}}",
        # TODO: change colour
        "\n{{yb:1: \"Purtroppo no.  Tu quando li hai visti l'ultima volta?\"}}",
        "{{yb:2: \"Non erano con te nel riparo nascosto?\"}}",
        "{{yb:3: \"(bugia) Sì, li ho visti in paese.\"}}",
        "\nUsa il comando {{lb:echo}} per parlare a Elenora."
    ]

    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]

    def check_command(self):
        if self.last_user_input in self.commands:
            return True
        elif self.last_user_input.startswith("echo"):
            text = (
                "\nEleonora: {{Bb:\"Scusa?  Che hai detto?\"}}"
            )
        else:
            text = (
                "\n{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} "
                "{{rb:o}} {{yb:echo 3}} {{rb:per rispondere.}}"
            )

        self.send_text(text)

    def next(self):
        Step3(self.last_user_input)


class Step3(StepMkdirEleanor):
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese"

    hints = [
        "{{rb:Usa}} {{yb:cd ../}} {{rb:per andare in paese.}}"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:Mamma mia, ci stiamo imbarcando in un'avventura!}}"
    )

    def __init__(self, prev_command="echo 1"):
        self.story = []

        if prev_command == "echo 1":
            self.print_text = [
                "{{yb:\"Purtroppo no. Quando li hai visti l'ultima volta?\"}}"
            ]
            self.story += [
                "Eleonora: {{Bb:\"Non molto tempo fa. Il cane è riscappato, "
                "allora sono andati fuori a cercarlo.\"}}"
            ]

        elif prev_command == "echo 2":
            self.print_text = [
                "{{yb:\"O non erano con te nel riparo nascosto?\"}}"
            ]
            self.story += [
                "Eleonora: {{Bb:No, sono andati fuori. "
                "Il cane è riscappato, allora sono andati fuori a cercarlo. "
                "Si saranno persi?\"}}"
            ]

        elif prev_command == "echo 3":
            self.print_text = [
                "{{yb:\"(bugia) S', li ho visti in paese.\"}}"
            ]
            self.story += [
                "Eleonora: {{Bb:\"Meno male! Il cane è riscappato, "
                "allora sono andati fuori a cercarlo.",
                "La campanella mi ha spaventato, ma sono contenta che stiano bene.\"}}"
            ]

        self.story += [
            "{{Bb:\"Andiamo insieme in paese a cercarli. Sono sicura di "
            "non avere problemi se sto con te.\"}}",

            "\n{{gb:Eleonora si è unita a te! Puoi controllare "
            "in ogni momento come sta con}} {{yb:cat Eleonora}}{{gb:.}}",

            "\n{{lb:Lascia}} il {{lb:.riparo-nascosto.}} "
            "Non ti preoccupare, Eleonora ti verrà dietro!"
        ]

        StepMkdirEleanor.__init__(self)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


class Step4(StepMkdirEleanor):
    start_dir = "~/paese"
    end_dir = "~/paese"
    hints = [
        "Eleonora: {{Bb:Ti sei dimenticato di guardare intorno? "
        "Devi usare}} {{yb:ls}}{{Bb:.}}",

        "{{rb:Guarda attorno con}} {{yb:ls}}{{rb:.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    deleted_items = ["~/paese/.riparo-nascosto/Eleonora"]

    story = [
        "Eleonora: {{Bb:Andiamo verso}} {{lb:est}}.",
#arf        "{{Bb:of paese.}}",
        "{{Bb:Non l'avevi vista prima? È proprio qui sopra! "
        "Guarda lassù.}}",
        "\nUsa {{yb:ls}} per vedere quello che ti sta mostrando Elenora."
    ]

    story_dict = {
        "Bernardo": {
            "path": "~/paese/est/negozio-di-capanni"
        },
        "miglior-fabbricatore-di-capanni-del-mondo.sh": {
            "path": "~/paese/est/negozio-di-capanni",
            "permissions": 0755
        },
        "miglior-clackson-del-mondo-scorretto.sh": {
            "name": "miglior-clackson-del-mondo.sh",
            "path": "~/paese/est/negozio-di-capanni",
            "permissions": 0755
        },
        "fotocopiatrice.sh, diario-di-bernardo-1, diario-di-bernardo-2": {
            "path": "~/paese/est/negozio-di-capanni/seminterrato"
        },
        "NANO": {
            "path": "~/paese/est/biblioteca/sezione-pubblica"
        },
        "private-section": {
            "path": "~/paese/est/biblioteca",
            # Remove all read and write permissions
            "permissions": 0000,
            "directory": True
        },
        "Clara": {
            "path": "~/paese/est/ristorante/.cantina"
        },
        "Eleonora": {
            "path": "~/paese"
        }
    }

    eleanors_speech = (
        "\nEleonora: {{Bb:Perché mi guardi? "
        "devi guardare LASSÙ.}}"
    )

    def next(self):
        Step5()


class Step5(StepMkdirEleanor):
    story = [
        "Guardi dove ti sta indidcando Elenora.",
        "C'è una piccola strada che conduce in un'altra zona del paese.",
        "Mi pare che vada dove sorge il sole, a est.",
        "Eleonora: {{Bb:Andiamo là a vedere se si trovano i miei "
        "genitori.}}",
        "\n{{lb:Vai verso}} l'{{lb:est}} del paese."
    ]
    start_dir = "~/paese"
    end_dir = "~/paese/est"

    hints = [
        "{{rb:Usa}} {{lb:cd}} {{rb:per andare verso "
        "l'est del paese}}",
        "{{rb:Usa}} {{yb:cd est/}} {{rb:}}"
    ]
    last_step = True

    eleanors_speech = (
        "\nEleonora: {{Bb:Andiamo verso l'}} {{lb:est}} "
        "{{Bb:del paese. Forza lumacone!}}"
    )

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        sys.exit("LAVORI IN CORSO! Traduzione in italiano arrivata fino a qui (1 ottobre 2015)\n")
        NextStep(self.xp)
