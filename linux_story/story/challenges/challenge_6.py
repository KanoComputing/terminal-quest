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
#arf        "Let Mum know about Dad. Type {{yb:cat Mum}}"
        "Diciamo alla mamma di questo fatto del babbo. Scrivi {{yb:cat mamma}}"
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    commands = "cat mamma"
    hints = (
#arf        "{{rb:To talk to your Mum, type}} {{yb:cat Mum}} {{rb:and press "
#arf        "Enter.}}"
        "{{rb:Per parlare alla mamma, scrivi}} {{yb:cat mamma}} {{rb:e premi "
        "Invio.}}"
    )

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
#arf        "{{wb:Mum:}} {{Bb:\"You couldn't find him? That's strange, "
        "{{wb:Mamma:}} {{Bb:\"Non l'hai trovato? Questo è strano, "
#arf        "he never leaves home without telling me first.\"",
        "non va mai via senza avvertirmi prima.\"",
#arf        "\"Maybe he went to that paese meeting with the Mayor,"
        "\"Forse è andato a quella riunione col sindaco in paese,"
#arf        " the one they were talking about on the news. "
        " quella che dicevano alla radio. "
#arf        "Why don't you go and check? I'll stay here in case he comes "
        "Perché non vai a controllare? Io rimango qui in caso ritorni.\"}}\n",
#arf        "back.\"}}\n",
#arf        "Let's head to {{bb:paese}}. To leave the house, use {{yb:cd}} by itself."
        "Andiamo allora in {{bb:paese}}. Per uscire di casa, usa {{yb:cd}} da solo."
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~"
    commands = "cd"
#arf    hints = "{{rb:Type}} {{yb:cd}} {{rb:to start the journey.}}"
    hints = "{{rb:Scrivi}} {{yb:cd}} {{rb:per andare.}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
#arf        "You're out of the house and on the long windy road called Tilde, "
#arf        "You're out of the house and on the long windy road called Tilde, "
        "Sei fuori di casa sulla lunga via centrale del paese, c'è vento.\n"
#arf        "or {{lb:~}}",
#arf        "{{lb:Look around}} again to see where to go next."
        "{{lb:Guarda in giro}} di nuovo per vedere dove andare."
    ]
    start_dir = "~"
    end_dir = "~"
    commands = "ls"
#arf    hints = "{{rb:Stuck? Type}} {{yb:ls}} {{rb:to look around.}}"
    hints = "{{rb:Problemi? Scrivi}} {{yb:ls}} {{rb:per guardare.}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
#arf        "You can see a {{bb:paese}} in the distance! Let's {{lb:go}} "
        "Si vede il {{bb:paese}} laggiù! {{lb:Andiamoci}} "
#arf        "there using {{lb:cd}}."
        "usando {{lb:cd}}."
    ]
    start_dir = "~"
    end_dir = "~/paese"
    commands = ["cd paese", "cd paese/"]
    hints = "{{rb:Type}} {{yb:cd paese/}} {{rb:to walk into paese.}}"

    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextChallengeStep(self.xp)
