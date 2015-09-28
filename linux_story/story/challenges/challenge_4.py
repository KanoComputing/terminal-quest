#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

# from linux_story.Step import Step
from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_5 import Step1 as NextChallengeStep
from linux_story.helper_functions import play_sound
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(TerminalCd):
    challenge_number = 4


class Step1(StepTemplateCd):
    story = [
        "Questo è molto strano. Ma non ho tempo di pensarci ora - vediamo dov'è la mamma.",
        "\n{{gb:Nuovo comando}}: con {{lb:cd}} ti puoi muovere da un posto all'altro.",
        "\nUsa il comando {{yb:cd ../}} per {{lb:lasciare}} la tua camera.\n"
    ]
    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia"
    commands = [
        "cd ..",
        "cd ../",
        "cd ~/casa-mia",
        "cd ~/casa-mia/"
    ]
    hints = [
        "{{rb:Scrivi}} {{yb:cd ../}} {{rb:per lasciare la tua camera. I due puntini sono}} "
        "{{lb:..}} "
        "{{rb:la stanza che trovi uscendo.}}",
        "{{rb:Scrivi}} {{yb:cd ../}} {{rb:per lasciare la tua camera.}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Hai lasciato {{bb:camera-mia}} e sei nell'ingresso di {{bb:casa-mia}}.",
        "{{lb:Guarda un po'}} che stanze ci sono, usa {{yb:ls}}.\n"
    ]
    start_dir = "~/casa-mia"
    end_dir = "~/casa-mia"
    commands = "ls"
    hints = "{{rb:Scrivi}} {{yb:ls}} {{rb:e premi Invio.}}"
    story_dict = {
        "foglietto_serra": {
            "name": "foglietto",
            "path": "~/casa-mia/giardino/serra"
        }
    }
    deleted_items = ['~/casa-mia/giardino/serra/babbo']

    def next(self):
        play_sound('bell')
        Step3()


class Step3(StepTemplateCd):
    story = [
        "{{pb:Ding. Dong.}}\n",
        "O questa?  Un campanello?  Un po' strano.",
        "Guardi verso la porta della {{bb:cucina}}, e senti rumori "
        "di qualcuno che sta cucinando.",
        "Sembra che qualcuno prepari la colazione!",
        "Per {{lb:andare in cucina}}, usa {{yb:cd cucina/}}"
    ]
    start_dir = "~/casa-mia"
    end_dir = "~/casa-mia/cucina"
    commands = ["cd cucina", "cd cucina/"]
    hints = ["{{rb:Scrivi}} {{yb:cd cucina/}} {{rb:e premi Invio.}}"]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Bravissimo, ora sei in cucina.",
        "{{lb:Cerca}} la mamma usando {{yb:ls}}."
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = "ls"
    hints = "{{rb:Non la trovi?  Scrivi}} {{yb:ls}} {{rb:e premi Invio.}}"

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "Eccola che lavora in una nuvola di vapore.",
        "{{lb:Sentiamo}} cos'ha da dire la {{lb:mamma}} "
        "usando {{lb:cat}}."
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = "cat mamma"
    hints = (
        "{{rb:Non sai che fare? Scrivi:}} {{yb:cat mamma}}. "
    )

    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
