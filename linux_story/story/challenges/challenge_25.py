#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_bernard import TerminalMkdirBernard
from linux_story.story.challenges.challenge_26 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateMkdir(TerminalMkdirBernard):
    challenge_number = 25


class Step1(StepTemplateMkdir):
    story = [
            "Bernardo: {{Bb:Ciao! Sssh, non dite nulla.}}",

        "{{Bb:So perché siete qui. Voi volete un capanno!",

        "Ho proprio quello che fa per voi. Ho il}} "
        "{{lb:miglior-fabbricatore-di-capanni-del-mondo.sh}}",

        "\nSembra decisamente entusiasta di questo attrezzo. {{lb:Guarda}} te stesso il "
        "{{lb:miglior-fabbricatore-di-capanni-del-mondo.sh}}",

        "\n{{gb:Usa il tasto TAB per scrivere più alla svelta.}}"
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"

    hints = [
        "{{rb:Usa}} {{lb:cat}} {{rb:vedere il}} "
        "{{lb:miglior-fabbricatore-di-capanni-del-mondo.sh}}",

        "{{rb:Usa}} {{yb:cat miglior-fabbricatore-di-capanni-del-mondo.sh}} "
        "{{rb:per esaminare l'attrezzo.}}"
    ]

    commands = [
        "cat miglior-fabbricatore-di-capanni-del-mondo.sh"
    ]
    eleanors_speech = (
        "Eleonora: {{Bb:Bernardo mi fa un po' paura...}}"
    )

    def check_command(self):
        if self.last_user_input == "cat miglior-clacson-del-mondo.sh":
            self.send_text(
                "\n{{rb:Stai cercando di leggere il file sbagliato! "
                "Tu vuoi leggere il}} {{lb:miglior-fabbricatore-di-capanni-del-mondo.sh}}"
                "{{rb:.}}"
            )
        else:
            return StepTemplateMkdir.check_command(self)

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
            "L'attrezzo ha una scritta: {{lb:mkdir capanno}}.",
        "Riconosci il comando {{lb:mkdir}}. È quello che hai usato "
        "per aiutare Romina nella fattoria.",

        "\nBernardo: {{Bb:È un attrezzo magico! Esegui il comando, "
        "e ti ritrovi il capanno.}}",

        "{{Bb:Provalo! Usalo con}} "
        "{{yb:./miglior-fabbricatore-di-capanni-del-mondo.sh}}",

        "\n{{gb:Usa TAB per fare prima a scrivere.}}"
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"

    hints = [
        "{{rb:Fai come dice Bernardo - usa}} "
        "{{yb:./miglior-fabbricatore-di-capanni-del-mondo.sh}} "
        "{{rb:per far girare il suo script (far funzionare il suo comando)}}"
    ]
    commands = [
        "./miglior-fabbricatore-di-capanni-del-mondo.sh"
    ]
    eleanors_speech = (
        "Eleonora: {{Bb:Ma non è come far girare}} "
        "{{yb:mkdir capanno}}{{Bb:?}}"
    )

    def check_command(self):
        if self.last_user_input == "./miglior-clacson-del-mondo.sh":
            self.send_text(
                "\n{{rb:Stai cercando di girare lo script sbagliato . "
                "Tu vuoi girare}} "
                "{{yb:./miglior-fabbricatore-di-capanni-del-mondo.sh}}"
            )
        else:
            return StepTemplateMkdir.check_command(self)

    def next(self):
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        "{{lb:Guardati attorno}} per vedere se hai creato un capanno."
    ]
    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per guardare attorno.}}"
    ]
    eleanors_speech = (
        "Eleonora: {{Bb:Ehi, guarda qua!}}"
    )

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Ha funzionato! Ora nella stanza c'è un nuovo capanno.",
        "Che succede se lo fai girare un'altra volta?",
        "{{gb:Premi il tasto SÙ due volte per ripetere il comando.}}"
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"

    hints = [
        "{{rb:Guarda che succede se giri lo script un'altra volta.}}",

        "{{rb:Gira lo script un'altra volta usando}} "
        "{{yb:./miglior-fabbricatore-di-capanni-del-mondo.sh}} "
        "{{rb:per vedere quello che succede.}}"
    ]
    commands = [
        "./miglior-fabbricatore-di-capanni-del-mondo.sh"
    ]
    eleanors_speech = (
        "Eleonora: {{Bb:Non credo che questo funzioni...}}"
    )

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
            "Ottieni questo errore: {{yb:mkdir: non puoi creare la cartella `capanno': "
        "Esiste già}}",
        "\nBernardo: {{Bb:Per forza non può funzionare la seconda volta - "
        "ce l'avete già un capanno!",

        "Sto lavorando alla prossima grande invenzione, il}} "
        "{{lb:miglior-clacson-del-mondo.sh}}{{Bb:.}}",

        "{{Bb:Serve ad avvertire tutti che stai arrivando. "
        "Ho qualche problema iniziale, "
        "ma sono sicuro che li risolverò presto.}}",

        "\n{{lb:Guarda il miglior-clacson-del-mondo.sh}} e vedi se "
        "trovi il problema.",

        "{{gb:Ricordati di usare il tasto TAB!}}"
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"
    commands = [
        "cat miglior-clacson-del-mondo.sh"
    ]

    hints = [
        "{{rb:Usa}} {{lb:cat}} {{rb:per esaminare l'attrezzo.}}",
        "{{rb:Usa}} {{yb:cat miglior-clacson-del-mondo.sh}} {{rb:per esaminare "
        "l'attrezzo.}}"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:A me pare che questo sia un po' rotto.}}"
    )

    def check_command(self):
        if self.last_user_input == "cat miglior-fabbricatore-di-capanni-del-mondo.sh":
            self.send_text(
                "\n{{rb:stai esaminando l'attrezzo sbagliato. Tu vuoi guardare "
                "il}} {{yb:miglior-clacson-del-mondo.sh}}"
            )

        else:
            return StepTemplateMkdir.check_command(self)

    def next(self):
        Step6()


class Step6(StepTemplateMkdir):
    story = [
        "Nell'attrezzo c'è scritto {{yb:eco \"Honk!\"}}",
        "Forse dovrebbe essere {{yb:echo \"Honk!\"}} invece...",
        "Come facciamo a aggiustare questo attrezzo?",
        "\nBernardo: {{Bb:Boia, ma voi ci chiappate.}}",
        "Eleonora: {{Bb:Se abbiamo bisogno di aiuto c'è la "
        "biblioteca, è giusto qui fuori.}}",
        "\nPrima di andare diamo un'{{lb:occhiata}} nel {{lb:seminterrato}}."
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"

    commands = [
        "ls seminterrato",
        "ls seminterrato/",
        "ls -a seminterrato",
        "ls -a seminterrato/",
    ]

    hints = [
        "{{rb:Usa}} {{lb:ls}} {{rb:per guardarci.}}",
        "{{rb:Usa}} {{yb:ls seminterrato/}} {{rb:per guardare dentro.}}"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:OooOOoh, ci sono dolci qui?}}"
    )

    def next(self):
        Step7()


class Step7(StepTemplateMkdir):
    story = [
        "Bernardo: {{Bb:Oooh birboni, voi non potete guardare qui.}}",
        "\n{{lb:Usciamo}} dal negozio di capanni e torniamo in paese."
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est"
    hints = [
        "{{rb:Esci dal negozio di capanni usando}} {{yb:cd ../}}"
    ]
    eleanors_speech = (
        "Eleonora: {{Bb:Wow, mi piace la biblioteca. Torniamo in paese!}}"
    )

    last_step = True

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)
