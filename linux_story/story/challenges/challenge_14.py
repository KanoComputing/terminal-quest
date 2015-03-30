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

from linux_story.Step import Step
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.common import tq_file_system
from linux_story.story.challenges.challenge_15 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_command_list


class StepTemplateMv(Step):
    challenge_number = 14

    def __init__(self, xp=""):
        Step.__init__(self, TerminalMv, xp)


class Step1(StepTemplateMv):
    story = [
        "Look around at the food available in the kitchen."
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{r:Use}} {{yb:ls}} {{rn:to have a look around the kitchen}}"
    ]

    def next(self):
        Step2()


# Move three pieces of food into the basket
class Step2(StepTemplateMv):
    story = [
        "Move three pieces of food into your basket",
        "You can move multiple items using {{yb:mv <item1> <item2>"
        " <item3> basket/}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    passable_items = [
        'banana',
        'cake',
        'croissant',
        'pie',
        'grapes',
        'milk',
        'sandwich'
    ]

    def block_command(self, line):
        line = line.strip()
        separate_words = line.split(' ')

        if "cd" in line:
            return True

        if separate_words[0] == 'mv' and (separate_words[-1] == 'basket' or
                                          separate_words[-1] == 'basket/'):
            for item in separate_words[1:-1]:
                if item not in self.passable_items:
                    return True

            return False

    def check_command(self, line, current_dir):
        line = line.strip()
        separate_words = line.split(' ')
        all_items = []

        if separate_words[0] == 'mv' and (separate_words[-1] == 'basket' or
                                          separate_words[-1] == 'basket/'):
            for item in separate_words[1:-1]:
                if item not in self.passable_items:
                    hint = (
                        '{{rb:You\'re trying to move something that isn\'t in'
                        ' the folder.\n Try using}} {{yb:mv %s basket/}}'
                        % self.passable_items[0]
                    )
                    self.send_hint(hint)
                    return

                else:
                    all_items.append(item)

            for item in all_items:
                self.passable_items.remove(item)

            hint = '{{gb:Well done!  Keep going.}}'

        else:
            hint = '{{rb:Try using}} {{yb:mv %s basket/}}' \
                % self.passable_items[0]

        self.send_hint(hint)

    # Check that the basket folder contains the correct number of files?
    def check_output(self, line):
        basket_dir = os.path.join(tq_file_system, 'my-house/kitchen/basket')
        food_files = [
            f for f in os.listdir(basket_dir)
            if os.path.isfile(os.path.join(basket_dir, f))
        ]

        if len(food_files) > 3:
            return True
        else:
            return False

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "\nNow we want to head back to the .hidden-shelter with the "
        "basket",
        "Move the {{yb:basket}} back to {{yb:~}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = [
        "mv basket ~",
        "mv basket/ ~",
        "mv basket ~/",
        "mv basket/ ~/"
    ]
    hints = [
        "{{rb:Use the command}} {{yb:mv basket ~}} "
        "{{rb:to move the basket to the road ~}}"
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "Follow the basket by using {{yb:cd}}"
    ]
    start_dir = "kitchen"
    end_dir = "~"
    command = [
        "cd",
        "cd ~",
        "cd ~/"
    ]
    hints = [
        "{{rb:Use the command}} {{yb:cd}} {{rb:by itself "
        "to move yourself to the road ~}}"
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Get the basket with all the food to the family. ",
        "Move the {{yb:basket}} to {{yb:town/.hidden-shelter}}",
    ]

    start_dir = "~"
    end_dir = "~"
    command = [
        "mv basket town/.hidden-shelter",
        "mv basket/ town/.hidden-shelter",
        "mv basket town/.hidden-shelter/",
        "mv basket/ town/.hidden-shelter/",
        "mv basket ~/town/.hidden-shelter",
        "mv basket/ ~/town/.hidden-shelter",
        "mv basket ~/town/.hidden-shelter/",
        "mv basket/ ~/town/.hidden-shelter/"
    ]
    hints = [
        "{{rb:Use}} {{yb:mv basket town/.hidden-shelter/}} "
        "{{rb:to move the basket to the family in need}}"
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step6()


class Step6(StepTemplateMv):
    story = [
        "{{gb:Nearly there!}} Go into {{yb:town/.hidden-shelter}} "
        "using {{yb:cd}}",
    ]

    start_dir = "~"
    end_dir = ".hidden-shelter"
    command = [
        "cd town/.hidden-shelter",
        "cd town/.hidden-shelter/",
        "cd ~/town/.hidden-shelter",
        "cd ~/town/.hidden-shelter/"
    ]
    hints = [
        "{{rb:Use}} {{yb:cd town/.hidden-shelter/}} "
        "{{rb:to be reunited with the family.}}",
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        "{{wn:Talk to the people using}} {{yb:cat}} {{wn:and see how they "
        "react to the food.}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    hints = [
        "Talk to everyone using {{yb:cat}}"
    ]
    allowed_commands = {
        "cat Edith": (
            "\n{{wb:Edith:}} {{Bb:You saved my little girl and my dog, "
            "and now you've saved us from starvation...how can I thank "
            "you?}}\n"
        ),
        "cat Eleanor": (
            "\n{{wb:Eleanor:}} {{Bb:Yummy! See, I told you doggy, "
            "someone would help us.}}\n"
        ),
        "cat Edward": (
            "\n{{wb:Edward:}} {{Bb:Thank you!  I knew you would come "
            "through for us.}}\n"
        ),
        "cat dog": (
            "\n{{wb:Dog:}} {{Bb:\"Woof!\"}} {{wn:\nThe dog seems very "
            "excited.\n}}"
        )
    }

    last_step = True

    def check_command(self, line, current_dir):
        if not self.allowed_commands:
            return True

        line = line.strip()

        if line in self.allowed_commands.keys():

            hint = self.allowed_commands[line]
            del self.allowed_commands[line]
            num_people = len(self.allowed_commands.keys())

            if num_people == 0:
                hint += '\n{{gb:Press Enter to continue.}}'

            # If the hint is not empty
            elif hint:
                hint += (
                    "\n{{gb:Talk to}} {{yb:" + str(num_people) +
                    "}} {{gb:other}}"
                )
                if num_people > 1:
                    hint += "{{gb:s}}"
        else:
            hint = (
                "{{rn:Use}} {{yb:" + self.allowed_commands.keys()[0] +
                "}} {{rn:to progress.}}"
            )

        self.send_hint(hint)

    def next(self):
        self.create_secret_chest()
        NextStep(self.xp)
