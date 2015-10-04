#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_bernard import TerminalMkdirBernard
from linux_story.story.challenges.challenge_27 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateMkdir(TerminalMkdirBernard):
    challenge_number = 26


class Step1(StepTemplateMkdir):
    story = [
        "Sei di nuovo in paese. Eleonora agita le braccia e indica "
        "un edificio distante.",
        "\n{{lb:Guardati intorno}} per vedere cosa sta indicando Eleonora."
    ]

    start_dir = "~/paese/est"
    end_dir = "~/paese/est"

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per guardarti attorno.}}"
    ]

    commands = [
        "ls",
        "ls -a"
    ]

    deleted_items = ["~/paese/est/negozio-di-capanni/Eleonora"]
    story_dict = {
        "Eleonora": {
            "path": "~/paese/est"
        }
    }
    eleanors_speech = "Eleonora: {{Bb:Ecco la biblioteca laggiù!}}"

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Ecco la  {{bb:biblioteca}}.",

        "Eleonora: {{Bb:Eccola! La}} {{bb:biblioteca}} "
        "{{Bb:è proprio qui!}} {{lb:Entriamo.}}"
    ]

    start_dir = "~/paese/est"
    end_dir = "~/paese/est/biblioteca"

    hints = [
        "{{rb:Usa}} {{yb:cd biblioteca/}} {{rb:per entrare nella biblioteca.}}"
    ]
    eleanors_speech = "Eleonora: {{Bb:Mi piace la biblioteca! Entriamo!}}"

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        "Eleonora si infila nella biblioteca e tu la segui.",
        "{{lb:Guarda intorno}} nella biblioteca."
    ]

    start_dir = "~/paese/est/biblioteca"
    end_dir = "~/paese/est/biblioteca"

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per guardarti attorno.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    deleted_items = ["~/paese/est/Eleonora"]
    story_dict = {
        "Eleonora": {
            "path": "~/paese/est/biblioteca"
        }
    }
    eleanors_speech = "Eleonora: {{Bb:È tutto echo-y-y-y-y..}}"

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Sei in un corridoio che conduce a due porte, ambedue hanno una scritta. "
        "Una ha l'iscrizione {{bb:sezione-pubblica}}, e l'altra "
        "{{bb:sezione-privata}}.",

        "Eleonora: {{Bb:Di solito c'era una bibliotecaria.",

        "Lei vorrebbe che io provassi a guardare nella}} "
        "{{bb:sezione-privata}}.",

        "{{Bb:Cosa pensi che ci sia qui?  Proviamo a}} "
        "{{lb:guardare dentro}}{{Bb:.}}"
    ]

    start_dir = "~/paese/est/biblioteca"
    end_dir = "~/paese/est/biblioteca"

    commands = [
        "ls sezione-privata/",
        "ls sezione-privata"
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls sezione-privata/}} {{rb:per guardare nella "
        "sezione-privata della biblioteca.}}"
    ]
    eleanors_speech = "Eleonora: {{Bb:Cosa c'è nella sezione-privata?}}"

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):

    story = [
        "Eleonora: {{Bb:Scommetto che la sezione-privata è chiusa "
        "per la gente di fuori...",

        "Vediamo se si trova qualcosa di utile nella}} "
        "{{bb:sezione-pubblica.}}",

        "\nUsa {{lb:ls}} per cercare nella {{lb:sezione-pubblica}}."
    ]

    start_dir = "~/paese/est/biblioteca"
    end_dir = "~/paese/est/biblioteca"
    commands = [
        "ls sezione-pubblica",
        "ls sezione-pubblica/",
        "ls -a sezione-pubblica",
        "ls -a sezione-pubblica/"
    ]
    hints = [
        "{{rb:Usa}} {{lb:ls}} {{rb:pre cercare nella sezione pubblica.}}",
        "{{rb:Usa}} {{yb:ls sezione-pubblica}} {{rb:per cercare nella"
        "sezione pubblica.}}"
    ]
    eleanors_speech = "Eleonora: {{Bb:Che c'è nella sezione-pubblica?}}"

    def next(self):
        Step6()


class Step6(StepTemplateMkdir):
    story = [
        "Eleonora: {{Bb:Ehi, sono spariti tutti i comandi.",
        "Mi domando se li ha rubati qualcuno?}}",

        "{{Bb:C'è n'e uno solo:}} {{lb:NANO}} {{Bb:. Cos'è?}}",
        "{{lb:Leggiamolo}} {{Bb:.}}"
    ]
    start_dir = "~/paese/est/biblioteca"
    end_dir = "~/paese/est/biblioteca"
    commands = [
        "cat sezione-pubblica/NANO"
    ]
    hints = [
        "{{rb:Esamina lo script NANO con}} {{yb:cat sezione-pubblica/NANO}}"
    ]
    eleanors_speech = (
        "Eleonora: {{Bb:Forse la biblioteca ha introdotto delle "
        "multe per i ritardi.}}"
    )

    def next(self):
        Step7()


class Step7(StepTemplateMkdir):
    story = [
        "Eleonora: {{Bb:Quindi nano ti consente di "
        "scrivere nei file?}}",

        "{{Bb:Allora si potrebbe usare per aggiustare quello "
        "script miglior-clacson-del-mondo.sh?}}",

        "{{Bb:Torniamo}} {{lb:indietro}} {{Bb:al}} {{lb:negozio-di-capanni}}{{Bb:.}}"
    ]
    start_dir = "~/paese/est/biblioteca"
    end_dir = "~/paese/est/negozio-di-capanni"
    eleanors_speech = (
        "Eleonora: {{Bb:...dobbiamo rivedere quel Bernardo antipatico?}}"
    )
    last_step = True

    path_hints = {
        "~/paese/est/biblioteca": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ../}} {{rb:per tornare indietro.}}"
        },
        "~/paese/est": {
            "not_blocked": "\n{{gb:Ottimo! Ora entra nel}} {{lb:negozio-di-capanni}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd negozio-di-capanni/}} {{rb:per andare nel negozio-di-capanni.}}"
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
        NextStep(self.xp)
