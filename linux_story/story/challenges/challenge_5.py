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
#arf        "{{wb:Mum:}} {{Bb:\"Hi sleepyhead, breakfast is nearly ready. "
        "{{wb:Mamma:}} {{Bb:\"Ciao dormigliona, la colazione è quasi pronta. "
#arf        " Can you go and grab your Dad?"
        " Puoi andare a chiamare il babbo?"
#arf        " I think he's in the}} {{bb:giardino}}{{Bb:.\"}}\n",
        " Penso che sia in}} {{bb:giardino}}{{Bb:.\"}}\n",
#arf        "Let's look for your Dad in the {{bb:giardino}}.",
        "Cerca il tuo babbo in {{bb:giardino}}.",
#arf        "First we need to {{lb:leave}} the cucina using {{yb:cd ../}}\n"
        "Prima bisogna {{lb:uscire}} dalla cucina usando {{yb:cd ../}}\n"
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia"
    commands = ["cd ..", "cd ../"]
    hints = "{{rb:To leave the cucina, type}} {{yb:cd ../}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
#arf        "You are back in the main hall of your house.",
        "Rieccoti nell'ingresso.",
#arf        "Can you see your {{bb:giardino}}?  Have a {{lb:look around}} you.\n"
        "Lo vedi dov'è il {{bb:giardino}}? {{lb:Dai un'occhiata intorno}}.\n"
    ]
    start_dir = "~/casa-mia"
    end_dir = "~/casa-mia"
    commands = "ls"
#arf    hints = "{{rb:Type}} {{yb:ls}} {{rb:to look around you.}}"
    hints = "{{rb:Scrivi}} {{yb:ls}} {{rb:per guardare attorno.}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
#arf        "You see doors to the {{bb:giardino}}, {{bb:cucina}}, "
        "Vedi le porte per {{bb:giardino}}, {{bb:cucina}}, "
#arf        "{{bb:camera-mia}} and {{bb:parents-room}}.",
        "{{bb:camera-mia}} e {{bb:camera-genitori}}.",
#arf        "{{lb:Go}} into your {{bb:giardino}}.\n"
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
#arf        "Use {{yb:ls}} to {{lb:look}} in the giardino for your Dad.\n"
        "Usa {{yb:ls}} per {{lb:vedere}} se il babbo è in giardino.\n"
    ]
    start_dir = "~/casa-mia/giardino"
    end_dir = "~/casa-mia/giardino"
    commands = "ls"
    hints = (
#arf        "{{rb:To look for your Dad, type}} {{yb:ls}} {{rb:and press "
#arf        "Enter.}}"
        "{{rb:Per cercare il babbo, scrivi}} {{yb:ls}} {{rb:e premi "
        "Invio.}}"
    )

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
#arf        "The {{bb:giardino}} looks beautiful at this time of year.",
        "Com'è bello il {{bb:giardino}} in questa stagione .",
#arf        "Hmmm...but you can't see him anywhere.",
        "Hmmm... ma non lo vedo da nessuna parte.",
#arf        "Maybe he's in the {{bb:serra}}.",
        "Forse è nella {{bb:serra}}.",
#arf        "\n{{lb:Go}} inside the {{lb:serra}}.\n"
        "\n{{lb:Vai}} nella {{lb:serra}}.\n"
    ]
    start_dir = "~/casa-mia/giardino"
    end_dir = "~/casa-mia/giardino/serra"
    commands = ["cd serra", "cd serra/"]
#arf    hints = "{{rb:To go to the serra, type}} {{yb:cd serra/}}"
    hints = "{{rb:Per andare nella serra, scrivi}} {{yb:cd serra/}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
#arf        "Is he here? {{lb:Look around}} with {{yb:ls}} to find out.\n"
        "È qui? {{lb:Guarda attorno}} con {{yb:ls}} per vedere.\n"
    ]
    start_dir = "~/casa-mia/giardino/serra"
    end_dir = "~/casa-mia/giardino/serra"
    commands = "ls"
#arf    hints = "{{rb:Type}} {{yb:ls}} {{rb:to look for your Dad.}}"
    hints = "{{rb:Scrivi}} {{yb:ls}} {{rb:per cercare il tuo babbo.}}"

    def next(self):
        Step7()


class Step7(StepTemplateCd):
    story = [
#arf        "Your dad has been busy, there are loads of vegetables here.",
        "Il tuo babbo ha lavorato, ci sono un sacco di verdure.",
#arf        "Hmmmm. He's not here. But there is something odd.",
        "Hmmmm. No, non è qui. La cosa non quadra.",
#arf        "You see a note on the ground.  Use {{yb:cat note}} to "
        "C'è un foglietto in terra.  Usa {{yb:cat foglietto}} per "
#arf        "{{lb:read}} what it says.\n"
        "{{lb:leggere}} che c'è scritto.\n"
    ]
    start_dir = "~/casa-mia/giardino/serra"
    end_dir = "~/casa-mia/giardino/serra"
    commands = "cat foglietto"
#arf    hints = "{{rb:Type}} {{yb:cat note}} {{rb:to see what the note says!}}"
    hints = "{{rb:Scrivi}} {{yb:cat foglietto}} {{rb:per vedere che c'è scritto!}}"

    def next(self):
        Step8()


class Step8(StepTemplateCd):
    story = [
#arf        "Going back is super easy. Just type {{yb:cd ../}} to go back the way "
#arf        "you came.\n"
        "Tornare indietro è facilissimo. Scrivi semplicemente {{yb:cd ../}} per tornare indietro.\n"
    ]
    start_dir = "~/casa-mia/giardino/serra"
    end_dir = "~/casa-mia/giardino"
    commands = ["cd ..", "cd ../"]
#arf    hints = "{{rb:Type}} {{yb:cd ../}} {{rb:to go back to the giardino.}}"
    hints = "{{rb:Scrivi}} {{yb:cd ../}} {{rb:per tornare in giardino.}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step9()


class Step9(StepTemplateCd):
    story = [
#arf        "You're back in the giardino. Use {{yb:cd ../}} again to"
        "Rieccoti in giardino. Usa {{yb:cd ../}} ancora per"
#arf        " {{lb:go back}} to the house.",
        " {{lb:tornare}} in casa.",
#arf        "{{gb:Top tip: Press the UP arrow key to replay your previous command.}}\n"
        "{{gb:Super consiglio: premi la freccia in sù per rifare lo stesso comando.}}\n"
    ]
    start_dir = "~/casa-mia/giardino"
    end_dir = "~/casa-mia"
    commands = ["cd ..", "cd ../"]
#arf    hints = "{{rb:Type}} {{yb:cd ../}} {{rb:to go back to the house.}}"
    hints = "{{rb:Scrivi}} {{yb:cd ../}} {{rb:per tornare in casa.}}"

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step10()


class Step10(StepTemplateCd):
    story = [
#arf        "Now {{lb:go}} back into the {{bb:cucina}} and see Mum.\n"
        "Ora {{lb:torna}} in {{bb:cucina}} dalla mamma.\n"
    ]
    start_dir = "~/casa-mia"
    end_dir = "~/casa-mia/cucina"
    commands = ["cd cucina", "cd cucina/"]
#arf    hints = "{{rb:Type}} {{yb:cd cucina/}} {{rb:to go back to the cucina.}}"
    hints = "{{rb:Scrivi}} {{yb:cd cucina/}} {{rb:per tornare in cucina.}}"

    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextChallengeStep(self.xp)
