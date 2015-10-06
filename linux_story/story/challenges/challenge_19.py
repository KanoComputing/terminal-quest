#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
import sys

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_20 import Step1 as NextStep


class StepTemplate(TerminalEcho):
    challenge_number = 19


class Step1(StepTemplate):
    username = os.environ['LOGNAME']
    story = [
        "Romina: {{Bb:Mi hai spaventato!",
        "Ma ti conosco?  La tua faccia mi è famigliare...",
        "Aspetta... tu sei il figliolo della}} {{lb:mamma}} {{Bb:nella casa qua vicino, vero?",
        "..."
        "Sì?  Ma ce l'hai la lingua?",
        "Non ti chiami}} {{yb:" + username + "}}{{Bb:?}}",
        "\n{{gb:Rispondi dicendo di sì mediante il comando}} {{yb:echo sì}} "
        "{{gb:oppure}} {{yb:echo no}}."
    ]

    # Story has been moved to
    hints = [
        "{{rb:Usa}} {{lb:echo}} {{rb:per rispondere alla sua "
        "domanda.}}",
        "{{rb:Rispondi dicendo di sì con il comando}} {{yb:echo sì}}{{rb:.}}"
    ]

    commands = [
        "echo sì",
        "echo Sì",
        "echo SÌ",
        "echo si",
        "echo Si",
        "echo SI"
    ]

    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"

    def check_command(self):

        if self.last_user_input == "echo no" or \
                self.last_user_input == "echo No" or \
                self.last_user_input == "echo NO":
            hint = (
                "Romina: {{Bb:\"Oh non ti sconvolgere, "
                "assomigli precisamente a lei.\"}}"
            )
            self.send_hint(hint)

        return StepTemplate.check_command(self)

    def next(self):
        Step2()


class Step2(StepTemplate):
    print_text = ["{{yb:Sì}}"]

    story = [
        "Romina: {{Bb:\"Ah, lo sapevo!\"}}",
        "{{Bb:\"Quindi tu abiti in quella piccola casa fuori del paese?}}",
        # TODO: see if this can appear as a block
        # TODO: change the colour of this.
        "{{yb:1: Sì}}",
        "{{yb:2: No}}",
        "{{yb:3: Non lo so}}",
        "\n{{gb:Usa}} {{yb:echo 1}}{{gb:,}} {{yb:echo 2}} {{gb:o}} "
        "{{yb:echo 3}} {{gb:per rispondere nel modo 1, 2 o 3.}}\n"
    ]

    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"
    commands = ["echo 1", "echo 2", "echo 3"]
    hints = [
        "{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} "
        "{{yb:echo 3}} {{rb:per rispondere a Romina.}}"
    ]

    def check_command(self):
        replies = {
            "echo sì": "1",
            "echo no": "2",
            "echo \"non lo so\"": "3",
            "echo non lo so": "3"
        }

        if self.last_user_input.lower() in replies:
            hint = [
                "\n{{rb:Se vuoi rispondere con \"" +
                self.last_user_input +
                "\", usa}} {{yb:echo " +
                replies[self.last_user_input.lower()] +
                "}}"
            ]
            self.send_text(hint)
        else:
            return StepTemplate.check_command(self)

    def next(self):
        Step3(self.last_user_input)


# Option here to add a little exerpt where she mentions her dog was
# chasing a rabbit, and that we have to find the dog.
# We could go to the woods here, but not enter them.
class Step3(StepTemplate):
    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"

    # echo 3 should NOT pass this level
    commands = [
        "echo 1",
        "echo 2"
    ]
    hints = [
        "Romina: {{Bb:\"Scusami? Che hai detto? "
        "Sai come usare il comando}} {{lb:echo}} {{Bb:, sì?\"}}",
        "{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} "
        "{{yb:echo 3}} {{rb:per rispondere.}}"
    ]

    def __init__(self, prev_command='echo 1'):
        if prev_command == "echo 1":  # yes
            self.print_text = ["{{yb:Sì}}"]
            self.story = ["Romina: {{Bb:\"Me l'immaginavo!\"}}"]
        elif prev_command == "echo 2":  # no
            self.print_text = ["{{yb:No}}"]
            self.story = ["Romina: {{Bb:Non dire bugie, io lo so.}}"]
        elif prev_command == "echo 3":  # I don't know
            self.print_text = ["{{yb:Io non lo so}}"]
            self.story = ["Romina: {{Bb:Non lo sai?  Questo è preccupante...}}"]

        self.story = self.story + [
            "\n{{Bb:Sei venuto passando dal paese? "
            "Hai visto mio marito lì?",
            "È un}} {{lb:brontolone}} {{Bb:di bell'aspetto, era andato "
            "in paese per via di quella riunione importante "
            "con il sindaco.}}",
            "\n{{yb:1: \"Mi dispiace, è sparito proprio mentre era davanti a me.\"}}",
            "{{yb:2: \"Non ho visto suo marito, ma oggi varia gente "
            "è sparita in paese.\"}}",
            "{{yb:3: \"Non ne so niente.\"}}",
            "\nRispondi in uno dei modi seguenti usando"
            "il comando {{lb:echo}} e il numero dell'opzione.\n"
        ]
        StepTemplate.__init__(self)

    def check_command(self):
        if self.last_user_input == "echo 1":  # Disappeared in front of me
            # go to next step
            return StepTemplate.check_command(self)

        elif self.last_user_input == "echo 2":  # I didn't see him
            hint = (
                "Romina: {{Bb:\"Ho come l'impressione che tu mi stia nascondendo "
                "qualcosa...\"}}"
            )
            self.send_hint(hint)
            return False

        elif self.last_user_input == "echo 3":  # I don't know anything
            hint = (
                "Romina: {{Bb:Davvero?  Sei sicuro di non avere visto un}} "
                "{{lb:brontolone}}{{Bb: in paese?}}"
            )
            self.send_hint(hint)
            return False

        else:
            # Show default hint
            self.send_hint()
            return False

    def next(self):
        Step4()


class Step4(StepTemplate):
    print_text = [
        "{{yb:\"Mi dispiace, è sparito mentre era davanti a me.\"}}"
    ]
    story = [
        "Romina: {{Bb:\"Ti è sparito davanti?? Oh no! "
        "L'avevano detto alla radio che stava sparendo gente "
        "...e ora che dovrei fare?\"}}",
        "\n{{yb:1: \"Qualcuno è sopravissuto nascondendosi da qualche parte.\"}}",
        "{{yb:2: \"Penso che lei debba andare a cercare suo marito\"}}\n"
    ]

    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"
    last_step = True

    commands = [
        "echo 1",
        "echo 2"
    ]

    hints = [
        "Romina: {{Bb:Che hai detto?  Mica ho capito.}}",
        "{{rb:Usa}} {{yb:echo 1}} {{rb:o}} {{yb:echo 2}} {{rb:per rispondere.}}"
    ]

    def check_command(self):
        if self.last_user_input == "echo 1":  # Correct response
            # Can we asssume this is alright?
            return True
        elif self.last_user_input == "echo 2":
            response = (
                "Romina: {{Bb:\"Ci andrei, ma ho paura di sparire anch'io."
                "\nPotrebbe anche tornare, quindi in questo caso "
                "è meglio che rimanga qui.  Non ti viene in mente "
                "qualcos'altro?\"}}"
            )
            self.send_hint(response)
        else:
            self.send_hint()

    def next(self):
        NextStep(self.xp)
