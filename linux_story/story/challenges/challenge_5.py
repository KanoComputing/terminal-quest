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
from linux_story.story.challenges.challenge_6 import Step1 as NextChallengeStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(TerminalCd):
    challenge_number = 5


class Step1(StepTemplateCd):
    story = [
        "{{wb:Mamma:}} {{Bb:\"Ciao dormigliona, la colazione è quasi pronta. "
        " Puoi andare a chiamare il babbo?"
        " Penso che sia in}} {{bb:giardino}}{{Bb:.\"}}\n",
        "Cerca il tuo babbo in {{bb:giardino}}.",
        "Prima bisogna {{lb:uscire}} dalla cucina usando {{yb:cd ../}}\n"
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia"
    commands = ["cd ..", "cd ../"]
    hints = "{{rb:Per uscire dalla cucina, scrivi}} {{yb:cd ../}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Rieccoti nell'ingresso.",
        "Lo vedi dov'è il {{bb:giardino}}? {{lb:Dai un'occhiata intorno}}.\n"
    ]
    start_dir = "~/casa-mia"
    end_dir = "~/casa-mia"
    commands = "ls"
    hints = "{{rb:Scrivi}} {{yb:ls}} {{rb:per guardare attorno.}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Vedi le porte per {{bb:giardino}}, {{bb:cucina}}, "
        "{{bb:camera-mia}} e {{bb:camera-genitori}}.",
        "{{lb:Vai}} in {{bb:giardino}}.\n"
    ]
    start_dir = "~/casa-mia"
    end_dir = "~/casa-mia/giardino"
    commands = ["cd giardino", "cd giardino/"]
    hints = "{{rb:Type}} {{yb:cd giardino/}} {{rb:to go into the giardino.}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Usa {{yb:ls}} per {{lb:vedere}} se il babbo è in giardino.\n"
    ]
    start_dir = "~/casa-mia/giardino"
    end_dir = "~/casa-mia/giardino"
    commands = "ls"
    hints = (
        "{{rb:Per cercare il babbo, scrivi}} {{yb:ls}} {{rb:e premi "
        "Invio.}}"
    )

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "Com'è bello il {{bb:giardino}} in questa stagione .",
        "Hmmm... ma non lo vedo da nessuna parte.",
        "Forse è nella {{bb:serra}}.",
        "\n{{lb:Vai}} nella {{lb:serra}}.\n"
    ]
    start_dir = "~/casa-mia/giardino"
    end_dir = "~/casa-mia/giardino/serra"
    commands = ["cd serra", "cd serra/"]
    hints = "{{rb:Per andare nella serra, scrivi}} {{yb:cd serra/}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "È qui? {{lb:Guarda attorno}} con {{yb:ls}} per vedere.\n"
    ]
    start_dir = "~/casa-mia/giardino/serra"
    end_dir = "~/casa-mia/giardino/serra"
    commands = "ls"
    hints = "{{rb:Scrivi}} {{yb:ls}} {{rb:per cercare il tuo babbo.}}"

    def next(self):
        Step7()


class Step7(StepTemplateCd):
    story = [
        "Il tuo babbo ha lavorato, ci sono un sacco di verdure.",
        "Hmmmm. No, non è qui. La cosa non quadra.",
        "C'è un foglietto in terra.  Usa {{yb:cat foglietto}} per "
        "{{lb:leggere}} che c'è scritto.\n"
    ]
    start_dir = "~/casa-mia/giardino/serra"
    end_dir = "~/casa-mia/giardino/serra"
    commands = "cat foglietto"
    hints = "{{rb:Scrivi}} {{yb:cat foglietto}} {{rb:per vedere che c'è scritto!}}"

    def next(self):
        Step8()


class Step8(StepTemplateCd):
    story = [
        "Tornare indietro è facilissimo. Scrivi semplicemente {{yb:cd ../}} per tornare indietro.\n"
    ]
    start_dir = "~/casa-mia/giardino/serra"
    end_dir = "~/casa-mia/giardino"
    commands = ["cd ..", "cd ../"]
    hints = "{{rb:Scrivi}} {{yb:cd ../}} {{rb:per tornare in giardino.}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step9()


class Step9(StepTemplateCd):
    story = [
        "Rieccoti in giardino. Usa {{yb:cd ../}} ancora per"
        " {{lb:tornare}} in casa.",
        "{{gb:Super consiglio: premi la freccia in sù per rifare lo stesso comando.}}\n"
    ]
    start_dir = "~/casa-mia/giardino"
    end_dir = "~/casa-mia"
    commands = ["cd ..", "cd ../"]
    hints = "{{rb:Scrivi}} {{yb:cd ../}} {{rb:per tornare in casa.}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step10()


class Step10(StepTemplateCd):
    story = [
        "Ora {{lb:torna}} in {{bb:cucina}} dalla mamma.\n"
    ]
    start_dir = "~/casa-mia"
    end_dir = "~/casa-mia/cucina"
    commands = ["cd cucina", "cd cucina/"]
    hints = "{{rb:Scrivi}} {{yb:cd cucina/}} {{rb:per tornare in cucina.}}"

    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextChallengeStep(self.xp)
