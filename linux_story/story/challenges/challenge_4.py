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
#arf         "That's weird. No time for that now though - lets find Mum.",
        "Questo è molto strano. Ma non ho tempo di pensarci ora - vediamo dov'è la mamma.",
#arf        "\n{{gb:New Spell}}: {{lb:cd}} lets you move between places.",
        "\n{{gb:Nuova magia}}: con {{lb:cd}} ti puoi muovere da un posto all'altro.",
#arf        "\nUse the command {{yb:cd ../}} to {{lb:leave}} your room.\n"
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
#arf        "{{rb:Type}} {{yb:cd ../}} {{rb:to leave your room. The}} "
        "{{rb:Scrivi}} {{yb:cd ../}} {{rb:per lasciare la tua camera. I due puntini sono}} "
        "{{lb:..}} "
#arf        "{{rb:is the room behind you.}}",
        "{{rb:la stanza che trovi uscendo.}}",
#arf        "{{rb:Type}} {{yb:cd ../}} {{rb:to leave your room.}}"
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
#arf        "You've left {{bb:camera-mia}} and are in the hall of {{bb:casa-mia}}.",
        "Hai lasciato {{bb:camera-mia}} e sei nell'ingresso di {{bb:casa-mia}}.",
#arf        "{{lb:Look around}} at the different rooms using {{yb:ls}}.\n"
        "{{lb:Guarda un po'}} che stanze ci sono, usa {{yb:ls}}.\n"
    ]
    start_dir = "~/casa-mia"
    end_dir = "~/casa-mia"
    commands = "ls"
#arf    hints = "{{rb:Type}} {{yb:ls}} {{rb:and press Enter.}}"
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
#arf        "What was that?  A bell?  That's a bit odd.",
        "O questa?  Un campanello?  Un po' strano.",
#arf        "You see the door to your {{bb:cucina}}, and hear the sound of "
        "Guardi verso la porta della {{bb:cucina}}, e senti rumori "
#arf        "cooking.",
        "di qualcuno che sta cucinando.",
#arf        "Sounds like someone is preparing breakfast!",
        "Sembra che qualcuno prepari la colazione!",
#arf        "To {{lb:go inside the cucina}}, use {{yb:cd kitchen/}}"
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
#arf        "Great, you're in the cucina.",
        "Bravissimo, ora sei in cucina.",
#arf        "{{lb:Look}} for Mum using {{yb:ls}}."
        "{{lb:Cerca}} la mamma usando {{yb:ls}}."
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = "ls"
#arf    hints = "{{rb:Can't find her?  Type}} {{yb:ls}} {{rb:and press Enter.}}"
    hints = "{{rb:Non la trovi?  Scrivi}} {{yb:ls}} {{rb:e premi Invio.}}"

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
#arf        "You see her busily working in a cloud of steam.",
        "Eccola che lavora in una nuvola di vapore.",
#arf        "Let's {{lb:listen}} to what {{lb:Mum}} has to say by "
        "{{lb:Sentiamo}} cos'ha da dire la {{lb:mamma}} "
#arf        "using {{lb:cat}}."
        "usando {{lb:cat}}."
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = "cat mamma"
    hints = (
#arf        "{{rb:Stuck? Type:}} {{yb:cat Mum}}. "
        "{{rb:Non sai che fare? Scrivi:}} {{yb:cat mamma}}. "
#arf        "{{rb:Don\'t forget the capital letter!}}"
    )

    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
