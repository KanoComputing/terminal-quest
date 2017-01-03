# challenge_14.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
import os
from kano.logging import logger
from linux_story.StepTemplate import StepTemplate
from linux_story.story.new_terminals.terminal_mv import TerminalMv
from linux_story.common import fake_home_dir
from linux_story.step_helper_functions import unblock_commands_with_cd_hint, unblock_commands


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        _("Let's {{lb:look around}} to see what food is available in the {{bb:kitchen}}.\n")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to have a}} {{lb:look around}} {{rb:the kitchen.}}")
    ]

    def next(self):
        return 14, 2


# Move three pieces of food into the basket
class Step2(StepTemplateMv):
    story = [
        _("{{lb:Move}} three pieces of food into your {{bb:basket}}.\n"),
        _("You can move multiple items using {{yb:mv <item1> <item2> <item3> basket/}}\n")
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
        "newspaper": _("{{rb:They asked for food, they probably shouldn't " +\
        "eat the newspaper.}}"),
        "oven": _("{{rb:This is a bit heavy for you to carry!}}"),
        "table": _("{{rb:This is a bit heavy for you to carry!}}")
    }
    moved_items = []

    def block_command(self, line):
        if not line:
            return False

        separate_words = line.split(' ')
        should_block = False

        if "cd" in line:
            return True   # block the CD command here
        elif "ls" in line:
            return False  # do not block the LS command

        if separate_words[0] == 'mv' and (separate_words[-1] == 'basket' or
                                          separate_words[-1] == 'basket/'):
            for item in separate_words[1:-1]:
                if item not in self.passable_items:
                    if item in self.unmovable_items:
                        self.send_hint(self.unmovable_items[item])
                        return True
                    else:
                        hint = _("{{rb:You\'re trying to move something that " +\
                                "isn\'t in the folder.\nTry using}} " +\
                                "{{yb:mv %s basket/}}") % self.passable_items[0]
                        self.send_hint(hint)
                        return True

        else:
            # print a message in the terminal to show that it failed
            print _("If you do not add the basket at the end of the command, " +\
                    "you will rename the items!")

        return should_block

    def check_command(self, line):
        separate_words = line.split(" ")
        all_items = []

        if separate_words[0] == 'mv' and (separate_words[-1] == 'basket' or
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
                hint = _("{{gb:Well done! Keep going.}}")

        else:
            hint = _("{{rb:Try using}} {{yb:mv %s basket/}}") % self.passable_items[0]

        self.send_hint(hint)

    # Check that the basket folder contains the correct number of files?
    def check_output(self, output):
        basket_dir = os.path.join(fake_home_dir, 'my-house/kitchen/basket')
        food_files = [
            f for f in os.listdir(basket_dir)
            if os.path.isfile(os.path.join(basket_dir, f))
        ]

        if len(food_files) > 3:
            return True
        else:
            return False

    def next(self):
        return 14, 3


class Step3(StepTemplateMv):
    story = [
        _("\nNow we want to head back to the {{bb:.hidden-shelter}} with the " +\
        "{{bb:basket}}."),
        _("{{lb:Move}} the {{bb:basket}} back to {{bb:~}}.\n")
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
        _("{{rb:Use the command}} {{yb:mv basket ~/}} {{rb:to move the basket to the windy road ~}}")
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 14, 4


class Step4(StepTemplateMv):
    story = [
        _("Follow the {{bb:basket}} by using {{yb:cd}}.\n")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~"
    commands = [
        "cd",
        "cd ~",
        "cd ~/"
    ]
    hints = [
        _("{{rb:Use the command}} {{yb:cd}} {{rb:by itself " +\
        "to move yourself to the road ~}}")
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 14, 5


class Step5(StepTemplateMv):
    story = [
        _("Now get the food-filled {{bb:basket}} to the family."),
        _("{{lb:Move}} the {{bb:basket}} to {{bb:town/.hidden-shelter}}."),
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
        _("{{rb:Use}} {{yb:mv basket town/.hidden-shelter/}} " +\
        "{{rb:to move the basket to the family.}}")
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 14, 6


class Step6(StepTemplateMv):
    story = [
        _("{{lb:Enter}} the {{bb:town/.hidden-shelter}} using {{yb:cd}}.\n"),
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
        _("{{rb:Use}} {{yb:cd town/.hidden-shelter}} " +\
        "{{rb:to be reunited with the family.}}"),
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 14, 7


class Step7(StepTemplateMv):
    story = [
        _("{{wn:Check on everyone with}} {{yb:cat}} {{wn:to see if " +\
        "they're happy with the food.}}\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    hints = [
        _("{{rb:Check on everyone using}} {{yb:cat}}")
    ]
    allowed_commands = {
        "cat Edith": \
            _("\n{{wb:Edith:}} {{Bb:\"You saved my little girl and my dog, " +\
            "and now you've saved us from starvation...how can I thank " +\
            "you?\"}}\n"),
        "cat Eleanor": \
            _("\n{{wb:Eleanor:}} {{Bb:\"Yummy! See, I told you doggy, " +\
            "someone would help us.\"}}\n"),
        "cat Edward": \
            _("\n{{wb:Edward:}} {{Bb:\"Thank you! I knew you would come " +\
            "through for us. You really are a hero!\"}}\n"),
        "cat dog": \
            _("\n{{wb:Dog:}} {{Bb:\"Woof!\"}} {{wn:\nThe dog seems very " +\
            "excited.\n}}")
    }

    def check_command(self, line):
        if not self.allowed_commands:
            return True

        if line in self.allowed_commands.keys():

            hint = self.allowed_commands[line]
            del self.allowed_commands[line]
            num_people = len(self.allowed_commands.keys())

            if num_people == 0:
                hint += _("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")

            # If the hint is not empty
            elif hint:
                if num_people > 1:
                    hint += _("\n{{gb:Check on}} {{yb:%d}} {{gb:others}}") % num_people
                else:
                    hint += _("\n{{gb:Check on}} {{yb:1}} {{gb:other}}")
        else:
            hint = _("{{rb:Use}} {{yb:%s}} {{rb:to progress.}}") % self.allowed_commands.keys()[0]

        self.send_hint(hint)

    def next(self):
        return 15, 1
