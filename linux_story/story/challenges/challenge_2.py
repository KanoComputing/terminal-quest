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

from linux_story.story.terminals.terminal_cat import TerminalCat
from linux_story.story.challenges.challenge_3 import Step1 as NextChallengeStep
from kano_profile.apps import save_app_state_variable


class StepCat(TerminalCat):
    challenge_number = 2


class Step1(StepCat):
    story = [
        "Ottimo, ora puoi vedere gli oggetti che ci sono attorno.",
        "C'è il tuo letto, una sveglia...",
        "Uffa...spengi quella sveglia!",
        "\n{{gb:Nuova magia}}: per {{lb:vedere}} gli oggetti, scrivi {{lb:cat}} "
#        "and the object name.",
        "e poi il nome dell'oggetto.",
#        "\nUse {{yb:cat alarm}} to {{lb:examine}} the alarm.\n",
        "\nUsa {{yb:cat sveglia}} per {{lb:vedere}} la sveglia.\n",

    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat alarm"
    hints = "{{rb:Scrivi}} {{yb:cat sveglia}} {{rb:per esaminare la sveglia.}}"

    def next(self):
        Step2()


class Step2(StepCat):
    story = [
#        "Ok - it's switched off. Better get dressed...",
        "Ovvia - tu l'hai spenta. Meglio vestirsi ora...",

#        "Type {{yb:ls wardrobe/}} to {{lb:look inside}} your "
        "Scrivi {{yb:ls armadio/}} per {{lb:guardare dentro}} il tuo "
#        "{{lb:wardrobe}}.\n"
        "{{lb:armadio}}.\n"
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = ["ls wardrobe", "ls wardrobe/"]
    hints = (
        "{{rb:Scrivi}} {{yb:ls armadio/}} {{rb:per cercare qualcosa "
        "metterti.}}"
    )

    def next(self):
        Step3()


class Step3(StepCat):
    story = [
#        "Check out that {{lb:t-shirt}}!",
        " Prova un po' quella {{lb:maglietta}}!",
#        "{{lb:Examine}} the t-shirt with {{yb:cat wardrobe/t-shirt}} "
        "{{lb:Guarda}} la maglietta con {{yb:cat armadio/maglietta}} "
#        "to see how it looks.\n"
        "per vedere un po' com'è.\n"
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat wardrobe/t-shirt"
    hints = (
#        "{{rb:Type}} {{yb:cat wardrobe/t-shirt}} "
        "{{rb:Scrivi}} {{yb:cat armadio/maglietta}} "
#        "{{rb:to investigate how it looks.}}"
        "{{rb:per vedere com'è."
    )

    def next(self):
        Step4()


class Step4(StepCat):
    story = [
#        "Looking good! Put that on and look for something else.",
        "Bellina! Mettitela e cerca qualcos'altro.",
#        "{{lb:Examine}} the {{lb:skirt}} or the {{lb:trousers}}.\n"
        "{{lb:Guarda un po'}} la {{lb:gonna}} o i {{lb:pantaloni}}.\n"
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = [
        "cat wardrobe/skirt",
        "cat wardrobe/trousers"
    ]
    hints = (
#        "{{rb:Type}} {{yb:cat wardrobe/trousers}} {{rb:or}} "
        "{{rb:Scrivi}} {{yb:cat armadio/pantaloni}} {{rb:o}} "
#        "{{yb:cat wardrobe/skirt}} {{rb:to dress yourself.}}"
        "{{yb:cat armadio/gonna}} {{rb:per vestirti.}}"
    )
    checked_outside_wardrobe = False

    def check_command(self):
        if self.last_user_input == self.commands[0]:
            save_app_state_variable('linux-story', 'outfit', 'skirt')
        elif self.last_user_input == self.commands[1]:
            save_app_state_variable('linux-story', 'outfit', 'trousers')
        elif not self.checked_outside_wardrobe and \
                (self.last_user_input == "cat trousers" or
                 self.last_user_input == "cat skirt"):
            self.send_text(
                "\n{{rb:You need to look in your}} {{lb:wardrobe}} "
                "{{rb:for that item.}}"
            )
            self.checked_outside_wardrobe = True

        return StepCat.check_command(self)

    def next(self):
        Step5()


class Step5(StepCat):
    story = [
#        "Awesome, your outfit is nearly complete.",
        "Benissimo, siamo quasi pronti.",
#        "Finally, check out that {{lb:cap}}.\n"
        "E ora guarda com'è il {{lb:berretto}}.\n"
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = [
        "cat wardrobe/cap"
    ]
    hints = (
#        "{{rb:Type}} {{yb:cat wardrobe/cap}} {{rb:to}} "
        "{{rb:Scrivi}} {{yb:cat armadio/berretto}} {{rb:per}} "
        "{{lb:vedere}} {{rb:il berretto.}}"
    )

    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
