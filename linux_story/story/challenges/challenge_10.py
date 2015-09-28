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
from linux_story.story.challenges.challenge_11 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(TerminalCd):
    challenge_number = 10


class Step1(StepTemplateCd):
    story = [
        "Sei in casa tua.  Pare che tu sia solo.",
        "Usa {{lb:cat}} per {{lb:esaminare}} qualche oggetto intorno a te.\n"
    ]
    allowed_commands = [
        "cat banana",
        "cat torta",
        "cat cornetto",
        "cat grappoli",
        "cat latte",
        "cat giornale",
        "cat stufa",
        "cat tortina",
        "cat panino",
        "cat tavolo"
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/casa-mia/cucina"
    counter = 0
    deleted_items = ["~/casa-mia/cucina/foglietto"]
    story_dict = {
        "Eleonora, Edoardo, Edith, mela, cane": {
            "path": "~/paese/.riparo-nascosto",
        },
        "bottiglia-vuota": {
            "path": "~/paese/.riparo-nascosto/cestino"
        },
        "MV": {
            "path": "~/paese/.riparo-nascosto/.piccolo-scrigno"
        }
    }
    # for check_command logic
    first_time = True

    def check_command(self):

        if self.last_user_input in self.allowed_commands:
            self.counter += 1
            self.allowed_commands.remove(self.last_user_input)
            hint = (
                "\n{{gb:Ottimo! Guarda giusto un altro "
                "oggetto.}}"
            )

        else:
            if self.first_time:
                hint = (
                    "\n{{rb:Usa}} {{lb:cat}} {{rb:per guardare due degli "
                    "oggetti.}}"
                )
            else:
                hint = (
                    '\n{{rb:Usa il comando}} {{yb:' + self.allowed_commands[0] +
                    '}} {{rb:per andare avanti.}}'
                )

        level_up = (self.counter >= 2)

        if not level_up:
            self.send_text(hint)
            self.first_time = False
        else:
            return level_up

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Non sembra esserci nient'altro che cibo, un sacco di cibo.",
        "Guarda se trovi qualcos'altro in {{bb:paese}}.",
        "Prima, usa {{yb:cd ../}} per {{lb:lasciare}} la cucina.\n"
    ]
    start_dir = "~/casa-mia/cucina"
    end_dir = "~/paese"
    commands = [
        "cd ~/paese",
        "cd ~/paese/",
        "cd ..",
        "cd ../",
        "cd paese",
        "cd paese/",
        "cd ../..",
        "cd ../../",
        "cd"
    ]
    num_turns_in_home_dir = 0

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def show_hint(self):

        # decide command needed to get to next part of paese
        if self.current_path == '~/casa-mia/cucina' or \
                self.current_path == '~/casa-mia':

            # If the last command the user used was to get here
            # then congratulate them
            if self.last_user_input == "cd .." or \
                    self.last_user_input == 'cd ../':
                hint = (
                    "\n{{gb:Buon lavoro! Ora ripeti l'ultimo comando "
                    "usando la freccia in sù della tastiera.}}"
                )

            # Otherwise, give them a hint
            else:
                hint = (
                    '\n{{rb:Usa}} {{yb:cd ../}} {{rb:per avviarti in paese.}}'
                )

        elif self.current_path == '~':
            # If they have only just got to the home directory,
            # then they used an appropriate command
            if self.num_turns_in_home_dir == 0:
                hint = (
                    "\n{{gb:Molto bene! Ora usa}} {{yb:cd paese/}} {{gb: "
                    "andare in paese.}}"
                )

            # Otherwise give them a hint
            else:
                hint = '\n{{rb:Usa}} {{yb:cd paese/}} {{rb:per andare in paese.}}'

            # So we can keep track of the number of turns they've been in the
            # home directory
            self.num_turns_in_home_dir += 1

        # print the hint
        self.send_text(hint)

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Usa {{yb:ls}} per {{lb:guardarti attorno}}.\n",
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls"
    hints = "{{rb:Usa}} {{yb:ls}} {{rb:per guardare quelle che c'è in paese.}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Sembra essere deserto.",
        "Ma ti sembra di sentire bisbigliare:",
        # TODO make this writing small
        "\n{{Bn:\".....se loro usano}} {{yb:ls -a}}{{Bn:, ci vedranno...\"}}",
        "{{Bn:\"..Shhh!  ...ci potrebbero sentire....\"}}\n"
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls -a"
    hints = [
        "{{rb:Hai sentito bisbigliare qualcosa a proposito del comando}} {{yb:ls -a}}"
        "{{rb:, provalo!}}",
    ]

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "Hai trovato un {{bb:.riparo-nascosto}} che non avevi notato prima.",
        "{{gb:Ciò che inizia con . non si vede normalmente.}}",
        "Sembra che proprio da qui vengano i bisbigli.  Prova a entrare.\n"
    ]
    start_dir = "~/paese"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "cd .riparo-nascosto",
        "cd .riparo-nascosto/"
    ]
    hints = [
        "{{rb:Prova a entrare nel}} {{lb:.riparo-nascosto}} {{rb:usando }}"
        "{{lb:cd}}{{rb:.}}",
        "{{rb:Usa il comando}} {{yb:cd .riparo-nascosto/ }}"
        "{{rb:per andare dentro.}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "C'è nessuno qui? Dai {{lb:un'occhiata}}.\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per guardare attorno.}}"
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
