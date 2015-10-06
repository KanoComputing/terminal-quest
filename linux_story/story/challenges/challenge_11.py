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

from linux_story.story.terminals.terminal_cd import TerminalCd

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_12 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands
from linux_story.common import tq_file_system


class StepTemplateCd(TerminalCd):
    challenge_number = 11


class StepTemplateMv(TerminalMv):
    challenge_number = 11


# The next few steps should be like the disappearing of people in the town
class Step1(StepTemplateCd):
    story = [
        "Toh... un gruppetto di gente spaventata e un cane....",
        "{{lb:Ascolta}} cosa dicono con {{lb:cat}}.\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"

    # Use functions here
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} {{Bb:\"Ci hanno trovati! Te l'avevo detto,  "
        "Edoardo, di parlare piano.\"}}",
        "cat Eleonora": "\n{{wb:Eleonora:}} {{Bb:\"La mia mamma ha paura "
        "che la campanella ci trovi se usciamo.\"}}",
        "cat Edoardo": "\n{{wb:Edoardo:}} {{Bb:\"Mi dispiace Edith...ma "
        "non credo che ci facciano del male.  Forse ci possono aiutare?\"}}",
        "cat cane": "\n{{wb:Cane:}} {{Bb:\"Bau bau!\"}}"
    }

    def check_command(self):

        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if self.last_user_input == 'ls':
            hint = "\n{{gb:Bravo, hai fatto la cosa giusta per guardarti attorno..}}"
            self.send_text(hint)
            return False

        # check through list of commands
        end_dir_validated = False
        self.hints = [
            "{{rb:Usa}} {{yb:" + self.all_commands.keys()[0] + "}} "
            "{{rb:per andare avanti.}}"
        ]

        end_dir_validated = self.current_path == self.end_dir

        # if the validation is included
        if self.last_user_input in self.all_commands.keys() and \
                end_dir_validated:
            # Print hint from person
            hint = "\n" + self.all_commands[self.last_user_input]

            self.all_commands.pop(self.last_user_input, None)

            if len(self.all_commands) > 0:
                hint += "\n{{gb:Ottimo! Controllane ancora " + \
                    str(len(self.all_commands)) + \
		    ".}}\n"
            else:
                hint += "\n{{gb:Premi Invio per continuare.}}"

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        # Don't pass unless the user has emptied self.all_commands
        return False

    def next(self):
        Step2()


# After we've heard some of the story from all the people
class Step2(StepTemplateMv):
    story = [
        "Edoardo ha l'aria di volerci dire qualcosa.\n",
        "{{wb:Edoardo:}} {{Bb:\"Ciao. Mi potresti aiutare?\"",

        "\"Avevo imparato questo comando per muovere le cose da"
        " un posto all'altro. Ma mi sembra che non funzioni.\"",

        "\"L'ho provato per mettere questa}} {{lb:mela}} {{Bb:nel}} "
        "{{lb:cestino}}{{Bb:\"}}",

        "{{Bb:\"M'avevano detto che il comando è}} {{yb:mv mela cestino/}}{{Bb:\"}}",

        "{{Bb:\"Ma non capisco che significa.  Lo devo dire? "
        "O scrivere?\"}}\n"
    ]

    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "mv mela cestino",
        "mv mela cestino/"
    ]
    hints = [
        "{{rb:Usa il comando}} {{yb:mv mela cestino/}} {{rb:per "
        "spostare la mela nel cestino.}}"
    ]
    # This is to add the apple into the virtual tree
    # we would like to integrate when using mv with the tree
    # automatically

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "Controlla se sei riuscito a spostare la mela. {{lb:guarda intorno}}.\n "
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per guardare intorno.}}"
    ]
    story_dict = {
        "mela": {
            "path": "~/paese/.riparo-nascosto/cestino"
        }
    }

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "{{gb:Buon lavoro! La mela non è più qui.}}\n",
        "{{wn:Ora controlla che la mela sia nel}} {{lb:cestino}} {{wn:usando}} "
        "{{lb:ls}}{{wn:.}}\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "ls cestino",
        "ls cestino/",
        "ls -a cestino",
        "ls -a cestino/"
    ]
    hints = [
        "{{rb:Usa il comando}} {{yb:ls cestino/}} {{rb:per guardare nel "
        "cestino.}}"
    ]

    def next(self):
        Step5()


# After cat-ing the person again?
class Step5(StepTemplateMv):
    story = [
        "{{gb:Eccellente, hai messo la mela nel cestino!}}",
        "\n{{wb:Edoardo:}} {{Bb:\"Ehi, ci sei riuscito! Che facevo di "
        "sbagliato?\"}}",
        "{{Bb:\"Puoi tirare fuori la mela dal cestino per rimetterla qui?\"}}\n",
        "{{lb:Sposta}} la {{lb:mela}} dal {{lb:cestino}} "
        "qui, dove ti trovi. Questo si indica con {{lb:./}}",
	"Così: {{yb:mv cestino/mela ./\n}} "
        "È necessario il {{lb:./}} !\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "mv cestino/mela .",
        "mv cestino/mela ./"
    ]
    hints = [
        "{{rb:Usa il comando}} {{yb:mv cestino/mela ./}} {{rb:per}} "
        "{{rb: spostare la mela dal cestino nella "
	"tua posizione attuale}} {{lb:./}}"
	]

    def block_command(self):
        if self.last_user_input == "mv cestino/cestino":
            hint = (
                "{{gb:Quasi! Il comando giusto è}} "
                "{{yb:mv cestino/mela ./}} {{gb:- non dimenticare il punto!}}"
            )
            self.send_hint(hint)
            return True
        else:
            return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step6()


class Step6(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{Bb:\"La dovete smettere di giocare con la mela, è  "
        "l'ultima cosa che ci resta da mangiare.\"}}",
        "{{Bb:\"Ah! il cane corre fuori!\"}}",
        "{{wb:Eleonora:}} {{Bb:\"Pippo!\"}}",
        "{{wb:Edith:}} {{Bb:\"No, amore!  Non uscire!\"}}",
        "\n{{lb:Eleonora}} segue il suo {{lb:cane}} uscendo dal "
        "{{lb:.riparo-nascosto}}.",
        "{{lb:Guarda intorno}} per controllare.\n"
    ]
    story_dict = {
        "Eleonora": {
            "path": "~/paese"
        },
        "cane": {
            "path": "~/paese"
        }
    }
    deleted_items = [
        '~/paese/.riparo-nascosto/Eleonora',
        '~/paese/.riparo-nascosto/cane'
    ]

    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "ls", "ls -a"
    ]
    hints = [
        "{{rb:Guarda attorno usando}} {{yb:ls}} {{rb:per controllare se Eleonora c'è.}} "
    ]

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{Bb:\"No!! Torna indietro, amore!!\"}}",
        "{{Bb:\"Ehi voi, salvate la mia bambina!\"}}\n",
        "Prima, {{lb:cerca fuori}} Elenora con {{yb:ls ../}}",

    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = ""
    commands = [
        "ls ..",
        "ls ../",
        "ls ~/paese",
        "ls ~/paese/"
    ]
    hints = [
        "{{rb:Guarda in paese usando}} {{yb:ls ../}} "
        "{{rb:oppure}} {{yb:ls ~/paese/}}"
    ]

    def next(self):
        Step8()


class Step8(StepTemplateMv):
    story = [
        "Ora {{lb:sposta Eleonora}} dal paese {{lb:..}} alla "
        "tua posizione attuale (riparo nascosto) {{lb:.}}\n"
    ]
    start_dir = "~/paese/.riparo-nascosto"
    end_dir = "~/paese/.riparo-nascosto"
    commands = [
        "mv ../Eleonora .",
        "mv ../Eleonora ./",
        "mv ~/paese/Eleonora ~/paese/.riparo-nascosto",
        "mv ~/paese/Eleonora ~/paese/.riparo-nascosto/",
        "mv ~/paese/Eleonora .",
        "mv ~/paese/Eleonora ./",
        "mv ../Eleonora ~/paese/.riparo-nascosto",
        "mv ../Eleonora ~/paese/.riparo-nascosto/",
    ]
    hints = [
        "{{rb:Veloce!  Usa}} {{yb:mv ../Eleonora ./}} "
        "{{rb:per riportare la bambina al sicuro.}}"
    ]
    last_step = True
    girl_file = os.path.join(tq_file_system, 'paese/.riparo-nascosto/Eleonora')

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def check_command(self):

        if os.path.exists(self.girl_file):
            return True

        else:
            self.send_hint()
            return False

    def next(self):
        NextStep(self.xp)
