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
#arf        "You're in your house.  You appear to be alone.",
        "Sei in casa tua.  Pare che tu sia solo.",
#arf        "Use {{lb:cat}} to {{lb:examine}} some of the objects around you.\n"
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
#arf                "\n{{gb:Well done!  Just look at one "
                "\n{{gb:Ottimo! Guarda giusto un altro "
#arf                "more item.}}"
                "oggetto.}}"
            )

        else:
            if self.first_time:
                hint = (
#arf                    "\n{{rb:Use}} {{lb:cat}} {{rb:to look at two of the "
                    "\n{{rb:Usa}} {{lb:cat}} {{rb:per guardare due degli "
#arf                    "objects around you.}}"
                    "oggetti.}}"
                )
            else:
                hint = (
#arf                    '\n{{rb:Use the command}} {{yb:' + self.allowed_commands[0] +
                    '\n{{rb:Usa il comando}} {{yb:' + self.allowed_commands[0] +
#arf                    '}} {{rb:to progress.}}'
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
#arf        "There doesn't seem to be anything here but loads of food.",
        "Non sembra esserci nient'altro che cibo, un sacco di cibo.",
#arf        "See if you can find something back in {{bb:paese}}.",
        "Guarda se trovi qualcos'altro in {{bb:paese}}.",
#arf        "First, use {{yb:cd ../}} to {{lb:leave}} the cucina.\n"
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
#arf                    "\n{{gb:Good work!  Now replay the last command using "
                    "\n{{gb:Buon lavoro! Ora ripeti l'ultimo comando "
#arf                    "the UP arrow on your keyboard.}}"
                    "usando la freccia in sù della tastiera.}}"
                )

            # Otherwise, give them a hint
            else:
                hint = (
#arf                    '\n{{rb:Use}} {{yb:cd ../}} {{rb:to make your way to paese.}}'
                    '\n{{rb:Usa}} {{yb:cd ../}} {{rb:per avviarti in paese.}}'
                )

        elif self.current_path == '~':
            # If they have only just got to the home directory,
            # then they used an appropriate command
            if self.num_turns_in_home_dir == 0:
                hint = (
#arf                    "\n{{gb:Good work! Now use}} {{yb:cd paese/}} {{gb: "
                    "\n{{gb:Molto bene! Ora usa}} {{yb:cd paese/}} {{gb: "
#arf                    "to head to paese.}}"
                    "andare in paese.}}"
                )

            # Otherwise give them a hint
            else:
#arf                hint = '\n{{rb:Use}} {{yb:cd paese/}} {{rb:to go into paese.}}'
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
#arf        "Use {{yb:ls}} to {{lb:look around}}.\n",
        "Usa {{yb:ls}} per {{lb:guardarti attorno}}.\n",
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls"
#arf    hints = "{{rb:Use}} {{yb:ls}} {{rb:to have a look around the paese.}}"
    hints = "{{rb:Usa}} {{yb:ls}} {{rb:per guardare quelle che c'è in paese.}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
#arf        "The place appears to be deserted.",
        "Sembra essere deserto.",
#arf        "However, you think you hear whispers.",
        "Ma ti sembra di sentire bisbigliare:",
        # TODO make this writing small
#arf        "\n{{Bn:\".....if they use}} {{yb:ls -a}}{{Bn:, they'll see us...\"}}",
        "\n{{Bn:\".....se loro usano}} {{yb:ls -a}}{{Bn:, ci vedranno...\"}}",
#arf        "{{Bn:\"..Shhh!  ...might hear....\"}}\n"
        "{{Bn:\"..Shhh!  ...ci potrebbero sentire....\"}}\n"
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls -a"
    hints = [
#arf        "{{rb:You heard whispers referring to}} {{yb:ls -a}}"
        "{{rb:Hai sentito bisbigliare qualcosa a proposito del comando}} {{yb:ls -a}}"
#arf        "{{rb:, try using it!}}",
        "{{rb:, provalo!}}",
    ]

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
#arf        "You see a {{bb:.riparo-nascosto}} that you didn't notice before.",
        "Hai trovato un {{bb:.riparo-nascosto}} che non avevi notato prima.",
#arf        "{{gb:Something that starts with . is normally hidden from view.}}",
        "{{gb:Ciò che inizia con . non si vede normalmente.}}",
#arf        "It sounds like the whispers are coming from there.  Try going in.\n"
        "Sembra che proprio da qui vengano i bisbigli.  Prova a entrare.\n"
    ]
    start_dir = "~/paese"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "cd .riparo-nascosto",
        "cd .riparo-nascosto/"
    ]
    hints = [
#arf        "{{rb:Try going inside the}} {{lb:.riparo-nascosto}} {{rb:using }}"
        "{{rb:Prova a entrare nel}} {{lb:.riparo-nascosto}} {{rb:usando }}"
        "{{lb:cd}}{{rb:.}}",
#arf        "{{rb:Use the command}} {{yb:cd .riparo-nascosto/ }}"
        "{{rb:Usa il comando}} {{yb:cd .riparo-nascosto/ }}"
#arf        "{{rb:to go inside.}}"
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
#arf        "Is anyone there? Have a {{lb:look around}}.\n"
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
        #arf
        sys.exit("LAVORI IN CORSO! Traduzione in italiano arrivata fin qui (25 settembre 2015)\n")
        #arf NextStep(self.xp)
