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
from linux_story.story.challenges.challenge_16 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateMv(TerminalMv):
    challenge_number = 15


class Step1(StepTemplateMv):
    story = [
        "Hai la sgradevole sensazione che ti manchi qualcosa.",
        "Qual'era quel comando che serviva a trovare questo luogo nascosto?",
        "Usalo per {{lb:guardare bene vicino}}.\n"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls -a}} {{rb:per guardare bene attorno.}}"
    ]

    story_dict = {
        "CAT, LS, CD, .foglietto": {
            "path": "~/casa-mia/camera-mia/.scrigno"
        }
    }

    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "ls -a"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "O questo cos'è! C'è un {{lb:.piccolo-scrigno}} in quell'angolo",
        "Dai un'{{lb:occhiata}} nel {{lb:.piccolo-scrigno}}."
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls .piccolo-scrigno}} {{rb:per guardare dentro}}"
    ]

    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "ls .piccolo-scrigno",
        "ls .piccolo-scrigno/",
        "ls -a .piccolo-scrigno",
        "ls -a .piccolo-scrigno/"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "C'è un frammento di pergamena dentro, con un timbro sopra: "
        "{{lb:MV}}.",
        "{{lb:Leggi}} cosa dice."
    ]

    hints = [
        "{{rb:Usa}} {{yb:cat .piccolo-scrigno/MV}} {{rb:per leggere la pergamena timbrata con MV}}"
    ]

    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "cat .piccolo-scrigno/MV"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "{{wb:Edoardo:}} {{Bb:\"Ehi, quello è il nostro}} {{lb:.piccolo-scrigno}}"
        "{{Bb:. Lo usiamo per tenere i nostri averi al sicuro. ",
        "Ho imparato come muovere gli oggetti grazie alle istruzioni}} "
        "{{Bb:su quella pergamena.",
        "Probabilmente serve di più a te. Prendila come ringraziamento.}}",
        "\nForse dovresti tornare a {{lb:casa-mia}} per cercare "
        "altri oggetti nascosti.",
        "Per tornare velocmente a casa, usa {{yb:cd ~/casa-mia/}}\n"
    ]

    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/casa-mia"
    commands = [
        'cd ~/casa-mia/',
        'cd ~/casa-mia'
    ]
    hints = [
        '{{rb:Non ci sono scorciatoie!  Usa}} {{yb:cd ~/casa-mia}} '
        '{{rb:per tornare a casa con un solo comando.}}'
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Vediamo se c'è qualcosa di nascosto anche qui!",
        "Dove pensi che ci possa essere qualcosa di nascosto?",
        "Proviamo a {{lb:guardare bene}} in {{lb:camera-mia}} prima."
    ]

    start_dir = '~/casa-mia'

    hints = [
        "{{rb:Bloccato?  Dai un'occhiata in}} {{yb:camera-mia}}{{rb:.}}",
        "{{rb:Usa}} {{yb:ls -a camera-mia}} {{rb:per cercare oggetti nascosti in}} "
        "{{lb:camera-mia}}{{rb:.}}"
    ]

    last_step = True

    def check_output(self, output):
        # Need to check that .scrigno is shown in the output of the command
        if not output:
            return False

        if '.scrigno' in output:
            return True

        return False

    def next(self):
        NextStep(self.xp)
