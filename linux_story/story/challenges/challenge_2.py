#!/usr/bin/env python
#
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
        _("Awesome, now you can see the objects around you."),
        _("There's your bed, an alarm..."),
        _("Euuughh...turn that alarm off!"),
        _("\n{{gb:New Spell}}: to {{lb:examine}} objects, type {{lb:cat}} "
        "and the object name."),
        _("\nUse {{yb:cat alarm}} to {{lb:examine}} the alarm.\n"),

    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat alarm"
    hints = _("{{rb:Type}} {{yb:cat alarm}} {{rb:to investigate the alarm.}}")

    def next(self):
        Step2()


class Step2(StepCat):
    story = [
        _("Ok - it's switched off. Better get dressed..."),

        _("Type {{yb:ls wardrobe/}} to {{lb:look inside}} your "
        "{{lb:wardrobe}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = ["ls wardrobe", "ls wardrobe/"]
    hints = (
        _("{{rb:Type}} {{yb:ls wardrobe/}} {{rb:to look for something "
        "to wear.}}")
    )

    def next(self):
        Step3()


class Step3(StepCat):
    story = [
        _("Check out that {{lb:t-shirt}}!"),
        _("{{lb:Examine}} the t-shirt with {{yb:cat wardrobe/t-shirt}} "
        "to see how it looks.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat wardrobe/t-shirt"
    hints = (
        _("{{rb:Type}} {{yb:cat wardrobe/t-shirt}} "
        "{{rb:to investigate how it looks.}}")
    )

    def next(self):
        Step4()


class Step4(StepCat):
    story = [
        _("Looking good! Put that on and look for something else."),
        _("{{lb:Examine}} the {{lb:skirt}} or the {{lb:trousers}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = [
        "cat wardrobe/skirt",
        "cat wardrobe/trousers"
    ]
    hints = (
        _("{{rb:Type}} {{yb:cat wardrobe/trousers}} {{rb:or}} "
        "{{yb:cat wardrobe/skirt}} {{rb:to dress yourself.}}")
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
                _("\n{{rb:You need to look in your}} {{lb:wardrobe}} "
                "{{rb:for that item.}}")
            )
            self.checked_outside_wardrobe = True

        return StepCat.check_command(self)

    def next(self):
        Step5()


class Step5(StepCat):
    story = [
        _("Awesome, your outfit is nearly complete."),
        _("Finally, check out that {{lb:cap}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = [
        "cat wardrobe/cap"
    ]
    hints = (
        _("{{rb:Type}} {{yb:cat wardrobe/cap}} {{rb:to}} "
        "{{lb:examine}} {{rb:the cap.}}")
    )

    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
