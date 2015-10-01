#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.helper_functions import play_sound
from linux_story.story.challenges.challenge_23 import Step1 as NextStep


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 22


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:Bravo, sembra che ci siano tutti!}}",
        "\nRomina: {{Bb:Grazie davvero!}}",
        "{{Bb:Staremo qui al sicuro.  Ti sono così grata per tutto quello "
        "che hai fatto.}}",
        "\nUsa {{lb:cat}} per controllare se gli animali stanno "
        "bene qui dentro"
    ]

    start_dir = "~/fattoria/fienile/.riparo"
    end_dir = "~/fattoria/fienile/.riparo"

    commands = [
        "cat Violetta",
        "cat Trogolo",
        "cat Gelsomino"
    ]
    hints = [
        "{{rb:Usa}} {{lb:cat}} {{rb:per controlare un animale, tipo}} "
        "{{yb:cat Violetta}}{{rb:.}}"
    ]

    # Remove all the food
    deleted_items = [
        "~/paese/.riparo-nascosto/basket",
        "~/paese/.riparo-nascosto/apple"
    ]

    def next(self):
        play_sound("bell")
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "{{pb:Ding. Dong.}}",
        "Romina: {{Bb:Cosa?? Ho sentito la campanella!  Che significa?}}",
        "\nSvelto! {{lb:Guarda attorno}} per controllare se manca qualcuno."
    ]

    start_dir = "~/fattoria/fienile/.riparo"
    end_dir = "~/fattoria/fienile/.riparo"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:guarda attorno con}} {{yb:ls}}{{rb:.}}"
    ]

    # Remove Edith
    deleted_items = [
        "~/paese/.riparo-nascosto/Edith"
    ]

    def next(self):
        play_sound("bell")
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        "Sembra che qui ci siano tutti...",
        "\n{{pb:Ding. Dong.}}",
        "\nRomina: {{Bb:Ancora! L'ho sentita! Ma è questa che hai sentito quando "
        "è sparito il mio marito?}}",
        "Dai un'altra {{lb:occhiata}} veloce."
    ]

    start_dir = "~/fattoria/fienile/.riparo"
    end_dir = "~/fattoria/fienile/.riparo"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Guardati attorno con}} {{yb:ls}}{{rb:.}}"
    ]
    # Remove Edoardo
    deleted_items = [
        "~/paese/.riparo-nascosto/Edoardo"
    ]

    def next(self):
        play_sound("bell")
        Step4()


# TODO: FIX THIS STEP
class Step4(StepTemplateMkdir):
    story = [
        "Romina: {{Bb:Meno male. Siamo al sicuro, qui ci sono tutti. "
        "Ma perché suona?}}",
        "\nForse dovremmo indagare su queste ultime suonate. Chi altro "
        "si conosceva?",
        "Si potrebbe rincontrollare quella famiglia rimpiattata nel "
        "{{lb:.riparo-nascosto}} e parlare loro, ora che hai la voce.",

        "\nInizia a tornare indietro per andare al {{lb:.riparo-nascosto}} con {{lb:cd}}"
    ]

    start_dir = "~/fattoria/fienile/.riparo"
    end_dir = "~/paese/.riparo-nascosto"

    hints = [
        "{{rb:Possiamo andare direttamente al}} {{lb:.riparo-nascosto}} "
        "{{rb:usando}} {{yb:cd ~/paese/.riparo-nascosto/}}"
    ]

    # Remove the cane
    deleted_items = [
        "~/paese/.riparo-nascosto/cane"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def check_command(self):
        # If the command passes, then print a nice hint.
        if self.last_user_input.startswith("cd") and \
                not self.get_command_blocked() and \
                not self.current_path == self.end_dir:
            hint = "\n{{gb:Ottimo! Continua così!}}"
            self.send_text(hint)
        else:
            return StepTemplateMkdir.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Guarda {{lb:attorno}}."
    ]

    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per guardare attorno.}}"
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
