#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os

# At this point, Bernardo disappears, so no need to keep blocking access to
# his basement.
from linux_story.story.terminals.terminal_eleanor import TerminalNanoEleanor
from linux_story.story.challenges.challenge_31 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepNano(TerminalNanoEleanor):
    challenge_number = 30


class Step1(StepNano):
    story = [
        "{{pb:Ding. Dong.}}",
        "\nEleonora: {{Bb:...questo cos'è?}}",
        "{{lb:Guarda attorno.}}"
    ]
    start_dir = "~/paese/est/ristorante/.cantina"
    end_dir = "~/paese/est/ristorante/.cantina"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per controllare che ci siano tutti.}}"
    ]
    deleted_items = [
        "~/paese/est/negozio-di-capanni/Bernardo"
    ]
    story_dict = {
        "cappello-di-bernardo": {
            "path": "~/paese/est/negozio-di-capanni"
        }
    }
    eleanors_speech = (
        "Eleonora: {{Bb:......}}"
    )

    def next(self):
        Step2()


class Step2(StepNano):
    story = [
        "Sembra che ci siano tutti. O cos'era allora quella campanella?",
        "\nSembra che Clara voglia dire qualcosa. {{lb:Ascoltala.}}"
    ]
    commands = [
        "cat Clara"
    ]
    start_dir = "~/paese/est/ristorante/.cantina"
    end_dir = "~/paese/est/ristorante/.cantina"
    hints = [
        "{{rb:Usa}} {{yb:cat Clara}} {{rb:per vedere cosa dice Clara.}}"
    ]
    eleanors_speech = (
        "Eleonora: {{Bb:....Ho avuto coì paura. Non credo di aver voglia "
        "di uscire ora.}}"
    )

    def next(self):
        Step3()


class Step3(StepNano):
    story = [
        "Clara: {{Bb:State andando fuori voi due?}}",
        "{{gb:" + os.environ['LOGNAME'] + "}}"
        "{{Bb:, sembra che tu sappia quello che fai, ma "
        "non mi piace l'idea che Eleonora esca.}}",
        "\n" + "{{gb:" + os.environ['LOGNAME'] + "}}"
        "{{Bb:, vuoi lasciare Eleonora con me? "
        "le farò compagnia.}}",
        "\n{{yb:1: Questa è una buona idea, occupati di lei allora.}}",
        "{{yb:2: No non mi fido, è più sicura con me.}}",
        "{{yb:3: (Chiedi a Eleonora.) Sei contenta di stare qui?}}",
        # "{{yb:4: Do you have enough food here?}}",
        "\n{{lb:Rispondi a Clara.}}"
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/paese/est/ristorante/.cantina"
    end_dir = "~/paese/est/ristorante/.cantina"
    hints = [
        "{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} "
        "{{yb:echo 3}} {{rb:per rispondere a Clara.}}"
    ]
    eleanors_speech = (
        "Eleonora: {{Bb:Sì, sono contenta di stare qui. Clara mi piace.}}"
    )

    def check_command(self):
        if self.last_user_input == "echo 2":
            text = (
                "\nClara: {{Bb:Per favore, lasciala con me. "
                "Non penso che sia sicuro per lei andare fuori.}}"
            )
            self.send_text(text)
        elif self.last_user_input == "echo 3":
            text = (
                "\nEleonora: {{Bb:Sono contenta di stare qui. Clara "
                "mi piace.}}"
            )
            self.send_text(text)
        # elif self.last_user_input == "echo 4":
        #    text = (
        #        "\nClara: {{Bb:There's loads of food here, look in the}} "
        #        "{{lb:larder}} {{Bb:if you don't believe me.}}"
        #    )
        #    self.send_text(text)
        else:
            return StepNano.check_command(self)

    def next(self):
        Step4()


class Step4(StepNano):
    story = [
        "Clara: {{Bb:Grazie!}}",
        "Eleonora: {{Bb:Se trovi i miei genitori, puoi dire loro "
        "che sono qui?}}",
        "Clara: {{Bb:E dove vuoi andare ora?}}",
        "\nTorna a vedere {{lb:Bernardo}} per saapere se ha sentito dire "
        "qualcosa dello {{lb:spadaccino mascherato}}.",
        "{{lb:Vai al negozio di capanni.}}"
    ]
    start_dir = "~/paese/est/ristorante/.cantina"
    end_dir = "~/paese/est/negozio-di-capanni"
    last_step = True

    path_hints = {
        "~/paese/est/ristorante/.cantina": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ../}} {{rb:per tornare indietro.}}"
        },
        "~/paese/est/ristorante": {
            "not_blocked": "\n{{gb:Ottimo! Continua così!}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd ../}} {{rb:per tornare indietro.}}"
        },
        "~/paese/est": {
            "not_blocked": "\n{{gb:Ora entra nel}} {{lb:negozio di capanni}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd negozio-di-capanni/}}{{rb:.}}"
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
