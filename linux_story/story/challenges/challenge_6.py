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
from linux_story.story.challenges.challenge_7 import Step1 as NextChallengeStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(TerminalCd):
    challenge_number = 6


class Step1(StepTemplateCd):
    story = [
        "Diciamo alla mamma di questo fatto del babbo. Scrivi {{yb:cat mamma}}"
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = "cat mamma"
    hints = (
        "{{rb:Per parlare alla mamma, scrivi}} {{yb:cat mamma}} {{rb:e premi "
        "Invio.}}"
    )

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "{{wb:Mamma:}} {{Bb:\"Non l'hai trovato? Questo è strano, "
        "non va mai via senza avvertirmi prima.\"",
        "\"Forse è andato a quella riunione col sindaco in paese,"
        " quella che dicevano alla radio. "
        "Perché non vai a controllare? Io rimango qui in caso ritorni.\"}}\n",
        "Andiamo allora in {{bb:paese}}. Per uscire di casa, usa {{yb:cd}} da solo."
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~"
    commands = "cd"
    hints = "{{rb:Scrivi}} {{yb:cd}} {{rb:per andare.}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Sei fuori di casa sulla lunga via centrale del paese, c'è vento.\n"
        "{{lb:Guarda in giro}} di nuovo per vedere dove andare."
    ]
    start_dir = "~"
    end_dir = "~"
    commands = "ls"
    hints = "{{rb:Problemi? Scrivi}} {{yb:ls}} {{rb:per guardare.}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Si vede il {{bb:paese}} laggiù! {{lb:Andiamoci}} "
        "usando {{lb:cd}}."
    ]
    start_dir = "~"
    end_dir = "~/paese"
    commands = ["cd paese", "cd paese/"]
    hints = "{{rb:Type}} {{yb:cd paese/}} {{rb:per andare in paese.}}"

    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextChallengeStep(self.xp)
