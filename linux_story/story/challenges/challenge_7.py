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
from linux_story.story.challenges.challenge_8 import Step1 as NextChallengeStep


class StepTemplateCd(TerminalCd):
    challenge_number = 7


class Step1(StepTemplateCd):
    story = [
        "{{lb:Diamo un'occhiata intorno}} per vedere che succede!"
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls"
    hints = "{{rb:Per guardare intorno, usa}} {{yb:ls}}"

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "Mamma mia quanta gente. Cerca il {{lb:sindaco}} e "
        "{{lb:ascolta}} che cos'ha da dire."
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "cat sindaco"
    hints = "{{rb:Bloccato? Scrivi:}} {{yb:cat sindaco}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "{{wb:sindaco:}} {{Bb:\"Calma per favore! I nostri uomini migliori "
        "stanno indagando sulle sparizioni, e speriamo di avere "
        "presto delle spiegazioni.\"}}\n",
        "Sta succedendo qualcosa di strano. Meglio controllare.",
        "Scrivi {{lb:cat}} per controllare cosa dicono le persone."
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"

    # Use functions here
    command = ""
    all_commands = {
        "cat brontolone": "\n{{wb:L'uomo:}} {{Bb:\"Aiuto! Non so cosa mi "
        "stia succedendo. Ho sentito suonare questa campana, e ora sento le "
        "mie gambe tutte strane.\"}}",
        "cat ragazzina": "\n{{wb:Ragazza:}} {{Bb:\"Mi puoi aiutare? Non riesco "
        "a trovare la mia amica Anna da nessuna parte. Se la vedi mi "
        " avverti?\"}}",
        "cat ragazzino": "\n{{wb:Ragazzo:}} {{Bb:\"Pongo? Pongo? Nessuno "
        "ha visto il mio cane Pongo? Non era mai scappato...\"}}"
    }

    last_step = True

    def check_command(self):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if self.last_user_input == 'ls':
            hint = "\n{{gb:Hai fatto la cosa giusto per guardarti attorno.}}"
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
        if (self.last_user_input in self.all_commands.keys()) and \
                end_dir_validated:
            # Print hint from person
            hint = "\n" + self.all_commands[self.last_user_input]

            self.all_commands.pop(self.last_user_input, None)

            if len(self.all_commands) == 1:
                hint += "\n{{gb:Ottimo! Controlla un'altra persona.}}\n"
            elif len(self.all_commands) > 0:
                hint += "\n{{gb:Ottimo! Controlla altre  " + \
                    str(len(self.all_commands)) + \
                    " persone.}}\n"
            else:
                hint += "\n{{gb:Premi Invio per continuare.}}"

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        NextChallengeStep(self.xp)
