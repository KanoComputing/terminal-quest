#!/usr/bin/env python
# coding: utf-8
#
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
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.challenges.challenge_17 import Step1 as NextStep
# import time


class StepTemplateMv(TerminalMv):
    challenge_number = 16


class Step1(StepTemplateMv):
    story = [
        "C'è uno {{lb:.scrigno}} antico nascosto sotto il tuo letto, "
        "che non ti ricordi d'avere mai visto.",
        "Vai in {{bb:camera-mia}} per guardare un po'.",
        "{{lb:Fruga}} nello {{lb:.scrigno}} e guarda se contiene qualcosa."
    ]

    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"

    commands = [
        'ls .scrigno',
        'ls .scrigno/',
        'ls -a .scrigno',
        'ls -a .scrigno/',
        'ls .scrigno/ -a',
        'ls .scrigno -a'
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls .scrigno}} {{rb:per guarddare in .scrigno}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "Ci sono dei rotoli di pergamena, simili a quello che hai trovato nel "
        " {{bb:.riparo-nascosto}}",
        "Usa {{lb:cat}} per {{lb:leggere}} uno dei rotoli.\n"
    ]

    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"

    commands = [
        'cat .scrigno/LS',
        'cat .scrigno/CAT',
        'cat .scrigno/CD'
    ]

    hints = [
        "{{rb:Usa}} {{yb:cat .scrigno/LS}} {{rb:per leggere la pergamena marcata con LS.}}"
    ]

    def next(self):
        Step3()


# Remove this step?
'''
class Step3(StepTemplateMv):
    story = [
        "Dovresti riconoscere questi comandi.",
        "Forse dovresti {{lb:spostare}} quello che avevi trovato in"
        "{{lb:~/paese/.riparo-nascosto/.piccolo-scrigno}} in questo {{lb:.scrigno}}, "
        "così sono tutti al sicuro nello stesso posto.",
        "\n{{gb:Usa il tasto TAB key per completare i percorsi dei file - risparmierai "
        "fatica alla tastiera!}}\n"
    ]

    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"

    commands = [
        "mv ~/paese/.riparo-nascosto/.piccolo-scrigno/MV .scrigno/",
        "mv ~/paese/.riparo-nascosto/.piccolo-scrigno/MV .scrigno",
        "mv ../../.riparo-nascosto/.piccolo-scrigno/MV .scrigno/",
        "mv ../../.riparo-nascosto/.piccolo-scrigno/MV .scrigno",
        "mv ~/paese/.riparo-nascosto/.piccolo-scrigno/MV ~/casa-mia/camera-mia/.scrigno/",
        "mv ~/paese/.riparo-nascosto/.piccolo-scrigno/MV ~/casa-mia/camera-mia/.scrigno"
    ]
    hints = [
        "{{rb:Vuoi usare il comando}} "
        "{{yb:mv ~/paese/.riparo-nascosto/.piccolo-scrigno/MV .scrigno/}}\n"
        "{{rb:Usa il tasto freccia in SÙ per ripetere il tuo ultimo comando "
        "se sei vicino!}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step4()
'''


class Step3(StepTemplateMv):
    story = [
        "Mi domando se ci sia altra roba nascosta in questo {{lb:.scrigno}}?",
        "cerca di nuovo {{lb:bene}} per vedere."
    ]

    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"

    hints = [
        "{{rb:Usa}} {{yb:ls -a .scrigno}} {{rb:per vedere se ci sono "
        "altre cose nascoste nello scrigno.}}"
    ]

    commands = [
        "ls -a .scrigno",
        "ls -a .scrigno/",
        'ls .scrigno/ -a',
        'ls .scrigno -a'
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "All'improvviso ti accorgi di un piccolo  {{lb:.foglietto}}, appallottolato "
        "in un angolo dello {{lb:.scrigno}}.",
        "Che dice?\n"
    ]

    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"

    hints = [
        "{{rb:Usa}} {{yb:cat .scrigno/.foglietto}} {{rb:per leggere il}} "
        "{{lb:.foglietto}}{{rb:.}}"
    ]

    commands = [
        "cat .scrigno/.foglietto"
    ]

    def next(self):
        NextStep(self.xp)
