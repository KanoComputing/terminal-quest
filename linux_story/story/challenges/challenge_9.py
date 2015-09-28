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

from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_10 import Step1 as NextStep
from linux_story.helper_functions import play_sound
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(TerminalCd):
    challenge_number = 9


class Step1(StepTemplateCd):
    story = [
        "Oh no! Controlla che la mamma stia bene.",
        "Scrivi {{yb:cd ../}} per andare via dal {{bb:paese}}."
    ]
    start_dir = "~/paese"
    end_dir = "~"
    commands = ["cd ..", "cd ../", "cd"]
    hints = "{{rb:Usa}} {{yb:cd ../}} {{rb:per iniziare a tornare a casa.}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        play_sound('bell')
        Step2()


class Step2(StepTemplateCd):
    story = [
        "{{pb:Ding. Dong.}}\n",

        "Scrivi {{yb:cd casa-mia/cucina/}} per andare direttamente in "
        "{{bb:cucina}}.",

        "{{gb:Premi TAB per scrivere più alla svelta!}}"
    ]
    start_dir = "~"
    end_dir = "~/casa-mia/cucina"
    commands = ["cd casa-mia/cucina", "cd casa-mia/cucina/"]
    hints = [
        "{{rb:Usa}} {{yb:cd casa-mia/cucina/}} {{rb:per andare in "
        "cucina.}}"
    ]
    story_dict = {
        "foglietto_cucina": {
            "name": "foglietto",
            "path": "~/casa-mia/cucina"
	    }
	}
    # Remove the foglietto as well.
    deleted_items = ['~/casa-mia/cucina/mamma', '~/paese/foglietto']

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Controlla attorno che sia tutto in ordine."
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = "ls"
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per controllare che sia "
        "a posto.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Oh no - è sparita anche la mamma!",
        "Aspetta, c'è un altro {{lb:foglietto}}.",
        "Usa {{lb:cat}} per {{lb:leggere}} il {{lb:foglietto}}."
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = "cat foglietto"
    hints = "{{rb:Usa}} {{yb:cat foglietto}} {{rb:per leggere foglietto.}}"
    last_step = True

    def next(self):
        NextStep(self.xp)
