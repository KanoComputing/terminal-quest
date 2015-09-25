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
#arf        "Have a {{lb:look around}} to see what's going on!"
        "{{lb:Diamo un'occhiata intorno}} per vedere che succede!"
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "ls"
#arf    hints = "{{rb:To look around, use}} {{yb:ls}}"
    hints = "{{rb:Per guardare intorno, usa}} {{yb:ls}}"

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
#arf        "Wow, there's so many people here. Find the {{lb:sindaco}} and "
        "Mamma mia quanta gente. Cerca il {{lb:sindaco}} e "
#arf        "{{lb:listen}} to what he has to say."
        "{{lb:ascolta}} che cos'ha da dire."
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"
    commands = "cat sindaco"
#arf    hints = "{{rb:Stuck? Type:}} {{yb:cat sindaco}}"
    hints = "{{rb:Bloccato? Scrivi:}} {{yb:cat sindaco}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
#arf        "{{wb:sindaco:}} {{Bb:\"Calm down please! We have our best "
        "{{wb:sindaco:}} {{Bb:\"Calma per favore! I nostri uomini migliori "
#arf        "people looking into the disappearances, and we're hoping to "
        "stanno indagando sulle sparizioni, e speriamo di avere "
#arf        "have an explanation soon.\"}}\n",
        "presto delle spiegazioni.\"}}\n",
#arf        "Something strange is happening. Better check everyone is ok.",
        "Sta succedendo qualcosa di strano. Meglio controllare.",
#arf        "Type {{lb:cat}} to check on the people."
        "Scrivi {{lb:cat}} per controllare le persone."
    ]
    start_dir = "~/paese"
    end_dir = "~/paese"

    # Use functions here
    command = ""
    all_commands = {
#arf        "cat grumpy-man": "\n{{wb:Man:}} {{Bb:\"Help! I don't know what's "
        "cat brontolone": "\n{{wb:L'uomo:}} {{Bb:\"Aiuto! Non so cosa mi "
#arf        "happening to me. I heard this bell ring, and now my legs have "
        "stia succedendo. Ho sentito suonare questa campana, e ora sento le "
#arf        "gone all strange.\"}}",
        "mie gambe tutte strane.\"}}",
#arf        "cat young-girl": "\n{{wb:Girl:}} {{Bb:\"Can you help me? I can't "
        "cat ragazzina": "\n{{wb:Ragazza:}} {{Bb:\"Mi puoi aiutare? Non riesco "
#arf        "find my friend Amy anywhere. If you see her, will you let me"
        "a trovare la mia amica Anna da nessuna parte. Se la vedi mi "
#arf        " know?\"}}",
        " avverti?\"}}",
#arf        "cat little-boy": "\n{{wb:Boy:}} {{Bb:\"Pongo? Pongo? Has "
        "cat ragazzino": "\n{{wb:Ragazzo:}} {{Bb:\"Pongo? Pongo? Nessuno "
#arf        "anyone seen my dog Pongo? He's never run away before...\"}}"
        "ha visto il mio cane Pongo? Non era mai scappato...\"}}"
    }

    last_step = True

    def check_command(self):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if self.last_user_input == 'ls':
#arf            hint = "\n{{gb:Well done for looking around.}}"
            hint = "\n{{gb:Hai fatto la cosa giusto per guardarti attorno.}}"
            self.send_text(hint)
            return False

        # check through list of commands
        end_dir_validated = False
        self.hints = [
#arf            "{{rb:Use}} {{yb:" + self.all_commands.keys()[0] + "}} "
            "{{rb:Usa}} {{yb:" + self.all_commands.keys()[0] + "}} "
#arf            "{{rb:to progress.}}"
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
#arf                hint += "\n{{gb:Well done! Check on 1 more person.}}\n"
                hint += "\n{{gb:Ottimo! Controlla un'altra persona.}}\n"
            elif len(self.all_commands) > 0:
#arf                hint += "\n{{gb:Well done! Check on " + \
                hint += "\n{{gb:Ottimo! Controlla altre  " + \
                    str(len(self.all_commands)) + \
                    " persone.}}\n"
            else:
#arf                hint += "\n{{gb:Press Enter to continue.}}"
                hint += "\n{{gb:Premi Invio per continuare.}}"

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        NextChallengeStep(self.xp)
