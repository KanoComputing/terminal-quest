#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_13 import Step1 as NextStep
from linux_story.common import tq_file_system
from linux_story.step_helper_functions import unblock_commands


class StepTemplateMv(TerminalMv):
    challenge_number = 12


# Thanks you for saving the little girl
class Step1(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{Bb:Grazie per averla salvata!}}",
        "{{wb:Eleonora:}} {{Bb:Pippo!}}",
        "{{wb:Edith:}} {{Bb:Potresti salvare anche il cane? Sono preoccupata "
        "che gli accada qualcosa se rimane fuori.}}\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "mv ../cane .",
        "mv ../cane ./",
        "mv ~/paese/cane ~/paese/.riparo-nascosto",
        "mv ~/paese/cane ~/paese/.riparo-nascosto/",
        "mv ~/paese/cane .",
        "mv ~/paese/cane ./",
        "mv ../cane ~/paese/.riparo-nascosto",
        "mv ../cane ~/paese/.riparo-nascosto/",
    ]
    hints = [
        "{{rb:Usa il comando}} {{yb:mv ../cane ./}} {{rb:per salvare il cane.}}"
    ]
    cane_file = os.path.join(tq_file_system, 'paese/.riparo-nascosto/cane')

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step2()


# Save both the cane and the little girl
class Step2(StepTemplateMv):
    story = [
        "{{wb:Eleonora:}} {{Bb:Ehi, Pippo!}}",
        "{{wb:Cane:}} {{Bb:Baubau!}}",
        "{{wb:Edith:}} {{Bb:Grazie davvero per averli recuperati tutti e due.",
        "Mi ero sbagliata su di te. Sei un eroe!}}\n",
        "{{lb:Ascolta tutti}} e guarda se c'è qualcun altro da aiutare.\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = "cat Edoardo"
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} {{Bb:\"Oh grazie! "
	"Eleonora, non andare a giro fuori un'altra volta - mi hai fatto "
        "morire di paura!\"}}",

        "cat Eleonora": "\n{{wb:Eleonora:}} {{Bb:\"Dove pensi che ci avrebbe "
        "portati la campanella?\"}}",

        "cat cane": "\n{{wb:Cane:}} {{Bb:\"Bau! Bau Bau!\"}}"
    }
    hints = [
        "{{gb:Sembra che Edoardo voglia dire qualcosa. "
        "Sentilo un po' usando}} {{yb:cat Edoardo}}"
    ]
    last_step = True

    def show_hint(self):
        if self.last_user_input in self.all_commands.keys():
            hint = self.all_commands[self.last_user_input]
            self.send_hint(hint)
        else:
            # Show default hints.
            self.send_hint()

    def next(self):
        NextStep(self.xp)
