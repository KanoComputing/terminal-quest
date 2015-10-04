#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_bernard import (
    TerminalMkdirBernard, TerminalNanoBernard
)
from linux_story.story.challenges.challenge_28 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateMkdir(TerminalMkdirBernard):
    challenge_number = 27


class StepTemplateNano(TerminalNanoBernard):
    challenge_number = 27


class Step1(StepTemplateMkdir):
    story = [
        "Rieccoti nel negozio di Bernardo.",
        "{{lb:Ascolta}} cosa dice {{lb: Bernardo}}."
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"

    hints = [
            "{{rb:Usa}} {{yb:cat Bernardo}} {{rb:per ascoltare Bernardo.}}"
    ]

    commands = [
        "cat Bernardo"
    ]

    deleted_items = ["~/paese/est/biblioteca/Eleonora"]
    story_dict = {
        "Eleonora": {
            "path": "~/paese/est/negozio-di-capanni"
        }
    }
    eleanors_speech = (
        "Eleonora: {{Bb:Etciuu! Quant'è polveroso questo posto...*sniff*}}"
    )

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "\nBernardo: {{Bb:Ciaooooo. Siete venuti a sistemare "
        "il mio script!}}",

        "Proviamo a usare {{yb:nano miglior-clacson-del-mondo.sh}} per "
        "editarlo (aggiustarlo)."
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"

    commands = [
        "nano miglior-clacson-del-mondo.sh"
    ]

    hints = [
        "{{rb:Usa}} {{yb:nano miglior-clacson-del-mondo}} "
        "{{rb:per editare (aggiustare).}}"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:È a scuola che ci hanno insegnato a scrivere. "
        "Non mi sembra molto intelligente Bernardo.}}"
    )

    goal_nano_end_content = "echo \"Honk!\""
    goal_nano_filepath = "~/paese/est/negozio-di-capanni/miglior-clacson-del-mondo.sh"
    goal_nano_save_name = "miglior-clacson-del-mondo.sh"

    # Overwrite the default behaviour for most of the steps - nano needs
    # slightly different behaviour.
    def check_command(self):
        if self.last_user_input == "cat Eleonora":
            self.send_text("\n" + self.eleanors_speech)
        else:
            return self.check_nano_input()

    def check_nano_content(self):
        return self.check_nano_content_default()

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Vai, è il momento di provare il tuo script!",
        "Usa {{yb:./miglior-clacson-del-mondo.sh}} per girarlo."
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"

    commands = [
        "./miglior-clacson-del-mondo.sh"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:Sarà abbastanza forte?}}"
    )
    hints = [
        "{{rb:Usa}} {{yb:./miglior-clacson-del-mondo.sh}} "
        "{{rb:per girare lo script.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    # Allow the user to ask all the questions within the same Step?
    story = [
        "{{gb:Congratulationi, ora lo script scrive \"Honk!\"}}",

        "\nBernardo: {{Bb:L'attrezzo funziona! Magnifico! "
        "Non so come ringraziarvi!}}",

        "\nTi rendi conto di non avere chiesto molto a Bernardo "
        "su se stesso.",

        "Che cosa ti piacerebbe domandargli?",

        "\n{{yb:1 \"Come hai fatto a creare i tuoi attrezzi?\"}}",

        "{{yb:2: \"Qual è il prossimo magnifico attrezzo che farai?\"}}",

        "{{yb:3: \"Ti stai per nascondere?\"}}",

        "{{yb:4: \"Cosa c'è nel tuo seminterrato?\"}}",

        "\nUsa {{lb:echo}} per fargli le domande."
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"
    hints = [
        "{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}}{{rb:,}} "
        "{{yb:echo 3}} {{rb:o}} {{yb:echo 4}}"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:Io ho una domanda - non è che ha delle caramelle "
        "nel suo seminterrato?}}"
    )

    commands = [
        "echo 2"
    ]

    def check_command(self):
        if self.last_user_input == "echo 1":
            text = (
                "\nBernardo: {{Bb:Ah, segreto commerciale. *occhiolino* ;-) }}"
            )
            self.send_text(text)
        elif self.last_user_input == "echo 3":
            text = (
                "\nBernardo: {{Bb:\"Eeh, Cosa? No, non l'ho previsto "
                "Perché dovrei?\"}}"
            )
            self.send_text(text)
        elif self.last_user_input == "echo 4":
            text = (
                "\nBernardo: {{Bb:Oh ho ho ho, questi non sono affari vostri.}}"
            )
            self.send_text(text)
        else:
            return StepTemplateNano.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    print_text = [
        "{{yb:\"Qual è il prossimo magnifico attrezzo che farai?\"}}"
    ]

    story = [
        "Bernardo: {{Bb:Voglio sapere come hanno fatto a chiudere la }} "
        "{{lb:sezione-privata}} {{Bb: della}} {{lb:biblioteca}}"
        "{{Bb:, e poi vorrei fare una chiave per aprirla.}}",

        "\nEleonora: {{Bb:Immagino che sia stata la bibliotecaria a chiudere la "
        "sezione privata.}}",

        "{{Bb:Forse ci potrebbe dire come ha fatto? Lo dovremmo "
        "cercare.}}",

        "\n{{lb:Esci}} dal negozio di capanni."
    ]

    hints = [
        "{{rb:Usa}} {{lb:cd}} {{rb:per uscire dal negozio di capanni.}}",
        "{{rb:Usa}} {{yb:cd ../}} {{rb:per}} {{lb:tornare}} {{rb:in paese.}}",
    ]
    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est"
    eleanors_speech = (
        "Eleonora: {{Bb:Che cosa pensi che sia nascosto nella sezione privata?}}"
        "\n{{Bb:Forse sarebbe meglio che Bernardo non lo veda...}}"
    )
    last_step = True

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)
