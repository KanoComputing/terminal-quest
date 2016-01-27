# challenge_14.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from kano.logging import logger

from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.common import tq_file_system
from linux_story.story.challenges.challenge_15 import Step1 as NextStep
from linux_story.step_helper_functions import \
    unblock_commands_with_cd_hint, unblock_commands


class StepTemplateMv(TerminalMv):
    challenge_number = 14


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        "Let's {{lb:look around}} to see what food is "
        "available in the {{bb:kitchen}}.\n"
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to have a}} {{lb:look around}} "
        "{{rb:the kitchen.}}"
    ]

    def next(self):
        Step2()


# Move three pieces of food into the basket
class Step2(StepTemplateMv):
    story = [
        "{{lb:Move}} three pieces of food into your {{bb:basket}}.\n",
        "You can move multiple items using {{yb:mv <item1> <item2>"
        " <item3> basket/}}\n"
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    passable_items = [
        'banana',
        'cake',
        'croissant',
        'pie',
        'grapes',
        'milk',
        'sandwich'
    ]
    unmovable_items = {
        "newspaper": "{{rb:They asked for food, they probably shouldn't "
        "eat the newspaper.}}",

        "oven": "{{rb:This is a bit heavy for you to carry!}}",

        "table": "{{rb:This is a bit heavy for you to carry!}}"
    }
    moved_items = []

    def block_command(self):
        separate_words = self.last_user_input.split(' ')
        should_block = True

        if "cd" in self.last_user_input:
            return True   # block the CD command here
        elif "ls" in self.last_user_input:
            return False  # do not block the LS command

        if separate_words[0] == 'mv' and (separate_words[-1] == 'basket' or
                                          separate_words[-1] == 'basket/'):
            for item in separate_words[1:-1]:
                if item not in self.passable_items:
                    if item in self.unmovable_items:
                        self.send_hint(self.unmovable_items[item])
                        break
                    else:
                        hint = (
                            "{{rb:You\'re trying to move something that "
                            "isn\'t in the folder.\nTry using}} "
                            "{{yb:mv %s basket/}}"
                            % self.passable_items[0]
                        )
                        self.send_hint(hint)
                        break

            should_block = False

        else:
            # print a message in the terminal to show that it failed
            print 'If you do not add the basket at the end of the command,' \
                  ' you will rename the items!'

        return should_block

    def check_command(self):
        separate_words = self.last_user_input.split()
        all_items = []

        if self.get_command_blocked():
            hint = '{{rb:Try using}} {{yb:mv %s basket/}}' \
                % self.passable_items[0]

        elif separate_words[0] == 'mv' and (separate_words[-1] == 'basket' or
                                            separate_words[-1] == 'basket/'):
            for item in separate_words[1:-1]:
                all_items.append(item)

            items_moved = 0
            hint = ''

            for item in all_items:
                try:
                    self.passable_items.remove(item)
                    items_moved += 1
                except ValueError as e:
                    logger.debug("Tried removing item {} from list. User might have"
                                 " made a typo - [{}]".format(item, e))

            if items_moved:
                hint = '\n{{gb:Well done! Keep going.}}'

        else:
            hint = '{{rb:Try using}} {{yb:mv %s basket/}}' \
                % self.passable_items[0]

        self.send_hint(hint)

    # Check that the basket folder contains the correct number of files?
    def check_output(self, output):
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
        "\nNow we want to head back to the {{bb:.hidden-shelter}} with the "
        "{{bb:basket}}.",
        "{{lb:Move}} the {{bb:basket}} back to {{bb:~}}.\n"
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = [
        "mv basket ~",
        "mv basket/ ~",
        "mv basket ~/",
        "mv basket/ ~/"
    ]
    hints = [
        "{{rb:Use the command}} {{yb:mv basket ~/}} "
        "{{rb:to move the basket to the windy road ~}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "Follow the {{bb:basket}} by using {{yb:cd}}.\n"
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~"
    commands = [
        "cd",
        "cd ~",
        "cd ~/"
    ]
    hints = [
        "{{rb:Use the command}} {{yb:cd}} {{rb:by itself "
        "to move yourself to the road ~}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Now get the food-filled {{bb:basket}} to the family.",
        "{{lb:Move}} the {{bb:basket}} to {{bb:town/.hidden-shelter}}.",
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
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
        "{{rb:to move the basket to the family.}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step6()


class Step6(StepTemplateMv):
    story = [
        "{{lb:Enter}} the {{bb:town/.hidden-shelter}} using {{yb:cd}}.\n",
    ]

    start_dir = "~"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "cd town/.hidden-shelter",
        "cd town/.hidden-shelter/",
        "cd ~/town/.hidden-shelter",
        "cd ~/town/.hidden-shelter/"
    ]
    hints = [
        "{{rb:Use}} {{yb:cd town/.hidden-shelter}} "
        "{{rb:to be reunited with the family.}}",
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        "{{wn:Check on everyone with}} {{yb:cat}} {{wn:to see if "
        "they're happy with the food.}}\n"
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    hints = [
        "{{rb:Check on everyone using}} {{yb:cat"
    ]
    allowed_commands = {
        "cat Edith": (
            "\n{{wb:Edith:}} {{Bb:\"You saved my little girl and my dog, "
            "and now you've saved us from starvation...how can I thank "
            "you?\"}}\n"
        ),
        "cat Eleanor": (
            "\n{{wb:Eleanor:}} {{Bb:\"Yummy! See, I told you doggy, "
            "someone would help us.\"}}\n"
        ),
        "cat Edward": (
            "\n{{wb:Edward:}} {{Bb:\"Thank you! I knew you would come "
            "through for us. You really are a hero!\"}}\n"
        ),
        "cat dog": (
            "\n{{wb:Dog:}} {{Bb:\"Woof!\"}} {{wn:\nThe dog seems very "
            "excited.\n}}"
        )
    }

    last_step = True

    def check_command(self):
        if not self.allowed_commands:
            return True

        if self.last_user_input in self.allowed_commands.keys():

            hint = self.allowed_commands[self.last_user_input]
            del self.allowed_commands[self.last_user_input]
            num_people = len(self.allowed_commands.keys())

            if num_people == 0:
                hint += '\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}'

            # If the hint is not empty
            elif hint:
                hint += (
                    "\n{{gb:Check on}} {{yb:" + str(num_people) +
                    "}} {{gb:other}}"
                )
                if num_people > 1:
                    hint += "{{gb:s.}}"
                else:
                    hint += "{{gb:.}}"
        else:
            hint = (
                "{{rb:Use}} {{yb:" + self.allowed_commands.keys()[0] +
                "}} {{rb:to progress.}}"
            )

        self.send_hint(hint)

    def next(self):
        NextStep(self.xp)
