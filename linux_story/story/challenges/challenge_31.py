#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import time
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateNano(TerminalNano):
    challenge_number = 31


class Step1(StepTemplateNano):
    story = [
        "Sei arrivato nel negozio di capanni. {{lb:Garda attorno.}}"
    ]
    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per guardare attorno.}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Huh, Bernardo non c'è.",

        "Mi domando dove sia andato.",

        "Che sia nel suo {{lb:seminterrato}}? {{lb:Andiamo}} giù."
    ]
    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni/seminterrato"
    hints = [
        "{{rb:Vai nel seminterrato con}} {{yb:cd seminterrato/}}"
    ]

    def check_command(self):
        if self.last_user_input == "cat cappello-di-bernardo":
            self.send_text(
                "\nO non è il cappello di Bernardo questo? "
                "Strano che l'abbia lasciato qui..."
            )
        else:
            return TerminalNano.check_command(self)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Sei sceso nel seminterrato di Bernardo. {{lb:Guarda attorno.}}"
    ]
    start_dir = "~/paese/est/negozio-di-capanni/seminterrato"
    end_dir = "~/paese/est/negozio-di-capanni/seminterrato"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Guarda attorno con}} {{yb:ls}}{{rb:.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "C'è qualcosa che sembra un altro attrezzo e due diari.",
        "{{lb:Vediamoli}}."
    ]
    start_dir = "~/paese/est/negozio-di-capanni/seminterrato"
    end_dir = "~/paese/est/negozio-di-capanni/seminterrato"
    commands = [
        "cat diario-di-bernardo-1",
        "cat diario-di-bernardo-2",
        "cat fotocopiatrice.sh"
    ]
    hints = [
        "{{rb:Usa}} {{lb:cat}} {{rb:per esaminare gli oggetti "
        "che ci sono intorno.}}"
    ]

    def check_command(self):
        if self.last_user_input in self.commands:
            self.commands.remove(self.last_user_input)

            if not self.commands:
                text = (
                    "\n{{gb:Premi Invio per continuare.}}"
                )
                self.send_text(text)

            else:
                text = (
                    "\n{{gb:Ottimo! Guarda gli altri oggetti.}}"
                )
                self.send_text(text)

        elif not self.last_user_input and not self.commands:
            return True

        else:
            return StepTemplateNano.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    story = [
        "Girato abbastanza. Andiamo a vedere se si trova lo "
        "{{lb:spadaccino maascherato}} nel bosco, e vediamo "
        "cosa ci può dire.",
        "\n{{gb:Premi Invio per continuare.}}"
    ]
    start_dir = "~/paese/est/negozio-di-capanni/seminterrato"
    end_dir = "~/paese/est/negozio-di-capanni/seminterrato"
    last_step = True

    def next(self):
        self.exit()

        time.sleep(3)
