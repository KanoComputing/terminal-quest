#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.step_helper_functions import (
    unblock_cd_commands
)
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_19 import Step1 as NextStep


class StepTemplate(TerminalEcho):
    challenge_number = 18


class Step1(StepTemplate):
    story = [
        "Ti rendi conto! Hai parlato a voce alta in una stanza vuota!",
        "{{gb:Ora hai la capacità di parlare!}}",
        "Forse con questo comando puoi parlare alle persone.",

        "\nAndiamo in ~ per trovare quella fattoria!",
        "Scrivi {{yb:cd}} da solo per uscire subito sulla straada ventosa {{lb:~}}"
    ]

    hints = [
        "{{rb:Usa}} {{yb:cd}} {{rb:da solo per andare in}} {{lb:~}}"
    ]

    start_dir = "~/casa-mia/camera-genitori"
    end_dir = "~"

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplate):
    story = [
        "Eccoti di nuovo sulla strada ventosa, che si estende senza fine in ambedue "
        "le direzioni. {{lb:Guarda attorno.}}"
    ]
    hints = [
        "{{rb:guarda attorno con}} {{yb:ls}}{{rb:.}}"
    ]

    commands = [
        "ls",
        "ls -a"
    ]
    start_dir = '~'
    end_dir = '~'

    def next(self):
        Step3()


class Step3(StepTemplate):
    story = [
        "Vedi laggiù lontano una piccola fattoria.",
        "{{lb:Andiamoci}}."
    ]

    start_dir = "~"
    end_dir = "~/fattoria"
    hints = [
        "{{rb:Use}} {{yb:cd fattoria/}} {{rb:to head to the fattoria.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


class Step4(StepTemplate):
    story = [
        "{{lb:Guarda intorno.}}"
    ]

    commands = "ls"
    start_dir = "~/fattoria"
    end_dir = "~/fattoria"
    hints = ["{{rb:Usa}} {{yb:ls}} {{rb:per guardare intorno.}}"]

    def next(self):
        Step5()


class Step5(StepTemplate):
    story = [
        "Sei alla fattoria, c'è un {{bb:fienile}}, la {{bb:casa}} e "
        "un grande  {{bb:capanno per gli attrezzi}}.",
        "La terra è tenuta bene e non ci sono erbacce, ci devono "
        "essere delle persone qui in giro.",
        "{{lb:Guarda attorno}} per vedere se trovi "
        "qualcuno con cui parlare."
    ]
    start_dir = "~/fattoria"
    end_dir = "~/fattoria"
    counter = 0

    def finished_challenge(self, line):
        output = self.check_output(self.last_cmd_output)
        if not output:
            # If Romina not in output, check if command is ls
            self.check_command()

        return output

    def output_condition(self, output):
        if 'Romina' in output:
            return True

        return False

    def check_command(self):
        if self.last_user_input == 'ls' or 'ls ' in self.last_user_input:
            self.counter += 1

            if self.counter >= 3:
                self.send_text(
                    "\n{{rb:Usa}} {{yb:ls fienile}} {{rb:per cercare nel fienile.}}"
                )
            if self.counter == 2:
                self.send_text(
                    "\n{{rb:Hai già cercato nel}} {{lb:fienile}}?"
                )
            elif self.counter == 1:
                self.send_text(
                    "\n{{rb:Non c'è nessuno qui. Dovresti guardare "
                    "da qualche altra parte.}}"
                )

        else:
            self.send_text("\n{{rb:Usa}} {{yb:ls}} {{rb:per guardare intorno.}}")

    def block_command(self):
        if "mv" in self.last_user_input:
            return True

    def next(self):
        Step6()


class Step6(StepTemplate):

    story = [
        "Nel fienile c'è una donna che governa gli animali.",
        "{{lb:Vai}} nel {{lb:fienile}} per vedere meglio."
    ]

    start_dir = "~/fattoria"
    end_dir = "~/fattoria/fienile"
    hints = [
        "{{rb:Usa}} {{yb:cd fienile/}} {{rb:per andare nel fienile.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step7()


class Step7(StepTemplate):

    story = [
        # "In the fienile, you see a woman tending some animals.",
        # "You walk into the fienile to have a closer look.",
        "{{lb:Senti}} che dicono nel fienile, con "
        "il comando {{lb:cat}}."
    ]

    # what is this?
    last_challenge = True

    all_commands = {
        "cat Romina": "Romina: {{Bb:Ah! Chi sei?!}}",
        "cat Gelsomino": "Gelsomino: {{Bb:Hiii.}}",
        "cat Trogolo": "Trogolo: {{Bb:Oink Oink.}}",
        "cat Violetta": "Violetta: {{Bb:Muuuuu.}}"
    }

    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"
    last_step = True

    hints = [
        "{{rb:Se hai dimenticato chi c'è nel fienile, usa}} "
        "{{yb:ls}} {{rb:per ricordatelo.}}"
    ]

    # TODO: move this into step_helper_functions, used a few too
    # many times outside.
    def check_command(self):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if self.last_user_input == 'ls':
            hint = "\n{{gb:Ottimo.}}"
            self.send_text(hint)
            return False

        # check through list of commands
        end_dir_validated = False
        end_dir_validated = self.current_path == self.end_dir

        # if the validation is included
        if self.last_user_input in self.all_commands.keys() and \
                end_dir_validated:

            # Print hint from person
            hint = "\n" + self.all_commands[self.last_user_input]

            self.all_commands.pop(self.last_user_input, None)

            if len(self.all_commands) == 1:
                hint += (
                    "\n{{gb:Bene! controllane ancora un altro.}}"
                )
            elif len(self.all_commands) > 0:
                hint += "\n{{gb:Bene! Controllane altri " + \
                    str(len(self.all_commands)) + \
                    ".}}"
            else:
                hint += "\n{{gb:Premi invio per continuare.}}"

            self.send_text(hint)

        else:
            if not self.hints:
                self.hints = [
                    "{{rb:Usa}} {{yb:" + self.all_commands.keys()[0] + "}} "
                    "{{rb:per andare avanti.}}"
                ]
            self.send_hint()
            self.hints.pop()

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        NextStep(self.xp)
