#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys
import time
import threading

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_9 import Step1 as NextChallengeStep
from linux_story.helper_functions import play_sound


class StepTemplateCd(TerminalCd):
    challenge_number = 8


class StepTemplateCdBell(StepTemplateCd):

    def play_bell_delay(self):
        time.sleep(3)
        play_sound('bell')

    def __init__(self, xp=""):
        t = threading.Thread(target=self.play_bell_delay)
        t.start()
        StepTemplateCd.__init__(self, xp)


class Step1(StepTemplateCd):

    story = [
        "{{pb:Ding. Dong.}}\n",
        "Sembra la campanella di prima.",
        "Usa {{yb:ls}} per {{lb:guardarti attorno}} di nuovo."
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls"
    hints = "{{rb:Usa}} {{yb:ls}} {{rb:per guardarti attorno.}}"
    deleted_items = ["~/paese/brontolone"]

    def __init__(self, xp=""):
        play_sound("bell")
        StepTemplateCd.__init__(self, xp)

    def next(self):
        # This was the code we had originally.  Did the bell ring properly?
        Step2()


class Step2(StepTemplateCdBell):

    story = [
        "{{wb:Ragazzino:}} {{Bb:Oddio! Quel}} {{lb:brontolone}} "
        "\n{{Bb:con le gambe buffe è sparito!}} "
        "{{Bb:Avete sentito suonare la campanella prima che sparisse??}}",
        "\n{{wb:Ragazzina:}} {{Bb:Ho paura...}}",
        "\n{{pb:Ding. Dong.}}\n",
        "{{wb:Ragazzina:}} {{Bb:Oh! l'ho sentita di nuovo!}}",
        "\nDai {{lb:un'occhiata in giro}} per controllare."
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls"
    hints = "{{rb:Usa}} {{yb:ls}} {{rb:per guardare attorno.}}"
    deleted_items = ["~/paese/ragazzino"]

    def next(self):
        Step3()


class Step3(StepTemplateCdBell):

    story = [
"{{wb:Ragazzina:}} {{Bb:Aspetta, c'era un}} {{lb:ragazzo}} "
        "{{Bb:qui...no?",
        "Ogni volta che la campanella suona, qualcuno sparisce!}}",
        "{{wb:Sindaco:}} {{Bb:Potrebbe essere appena andato a casa...?}}",
        "\n{{pb:Ding. Dong.}}\n",
        "{{lb:Guarda intorno.}}"
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls"
    hints = "{{rb:Usa}} {{yb:ls}} {{rb:per guardare intorno.}}"
    deleted_items = ["~/paese/ragazzina"]

    def next(self):
        Step4()


class Step4(StepTemplateCd):

    story = [
        "Sei solo con il sindaco.",
        "{{lb:Ascolta}} ciò che ha da dire il sindaco."
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "cat sindaco"
    hints = "{{rb:Usa}} {{yb:cat sindaco}} {{rb:per parlare al sindaco.}}"

    def next(self):
        Step5()


class Step5(StepTemplateCdBell):

    story = [
        "{{wb:sindaco:}} {{Bb:\"Sono tutti...spariti??\"",
        "....Avrei da andare a casa ora...}}",
        "\n{{pb:Ding. Dong.}}\n"
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls"
    hints = "{{rb:Usa}} {{yb:ls}} {{rb:per guardare intorno.}}"
    deleted_items = ["~/paese/sindaco"]
    story_dict = {
        "foglietto_paese": {
            "name": "foglietto",
            "path": "~/paese"
        }
    }

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "Sono andati tutti via.",
        "Aspetta - c'è un foglietto per terra.",
        "Usa {{lb:cat}} per leggere il foglietto."
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "cat foglietto"
    hints = "{{rb:Usa}} {{yb:cat foglietto}} {{rb:per leggere il foglietto.}}"
    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
