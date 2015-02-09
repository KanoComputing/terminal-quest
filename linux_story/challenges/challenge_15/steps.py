#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.Step import Step
from linux_story.challenges.challenge_11.terminals import TerminalMv
from linux_story.file_data import HIDDEN_DIR


class StepTemplateMv(Step):
    challenge_number = 15

    def __init__(self):
        Step.__init__(self, TerminalMv)


# When you talk to Graham
class Step1(StepTemplateMv):
    story = [
        "{{wb:Edward:}} \"Hey, since you don't seem to be affected by going"
        " outside, can you gather some food for us?\"",
        "\"We didn't have time to grab any before we went into hiding. "
        "Do you remember seeing any food in your travels?\"\n",
        "...ah!  You have all that food in your {{yb:kitchen}}!",
        "We could give that to this family.",
        "Start by moving the basket to your house."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "mv basket ../../my-house/kitchen",
        "mv basket ../../my-house/kitchen/",
        "mv basket ~/my-house/kitchen",
        "mv basket ~/my-house/kitchen/",
    ]
    hints = [
        "{{r:Use the command}} {{yb:mv basket ~/my-house/kitchen}} "
        "{{rn:to move the basket to your kitchen}}"
    ]
    basket_file = os.path.join(HIDDEN_DIR, 'my-house/kitchen/basket')

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

    def check_output(self, line):
        return os.path.exists(self.basket_file)

    def next(self):
        Step2()


# Go back to your kitchen
class Step2(StepTemplateMv):
    story = [
        "Now head back to your kitchen."
    ]
    start_dir = ".hidden-shelter"
    end_dir = "kitchen"
    command = [
        "cd",
        "cd ..",
        "cd ../"
        "cd my-house",
        "cd my-house/",
        "cd kitchen",
        "cd kitchen/",
        "cd ../../my-house/kitchen",
        "cd ../../my-house/kitchen/",
        "cd ~/my-house/kitchen",
        "cd ~/my-house/kitchen/",
        "cd my-house/kitchen",
        "cd my-house/kitchen/",
        "cd ../..",
        "cd ../../"
    ]
    hints = [
        "{{r:Use the}} {{yb:cd}} {{rn:command to go back to your kitchen.}}"
    ]
    num_turns_in_home_dir = 0

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

    def show_hint(self, line, current_dir):

        # decide command needed to get to next part of town
        if current_dir == 'town' or current_dir == '.hidden-shelter':

            # If the last command the user used was to get here
            # then congratulate them
            if line == "cd .." or line == 'cd':
                hint = "{{gb:Good work!  Keep going!}}"

            # Otherwise, give them a hint
            else:
                hint = (
                    '{{r:Use}} {{yb:cd ..}} {{rn:to make your way to your}} '
                    '{{yb:kitchen}}'
                )

        elif current_dir == '~':
            # If they have only just got to the home directory,
            # then they used an appropriate command
            if self.num_turns_in_home_dir == 0:
                hint = "{{gb:Good work!  Keep going!}}"

            # Otherwise give them a hint
            else:
                hint = (
                    '{{r:Use}} {{yb:cd my-house/kitchen}} {{rn:to go into '
                    'your house}}'
                )

            # So we can keep track of the number of turns they've been in the
            # home directory
            self.num_turns_in_home_dir += 1

        # print the hint
        self.send_hint(hint)

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "Have a look to remind yourself of the food we have"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{r:Use}} {{yb:ls}} {{rn:To have a look around the kitchen}}"
    ]

    def next(self):
        Step4()


# Move three pices of food into the basket
class Step4(StepTemplateMv):
    story = [
        "Move three pieces of food into your basket"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    other_commands = [
        "mv banana basket",
        "mv banana basket/",
        "mv crossaint basket",
        "mv crossaint basket/",
        "mv cake basket",
        "mv cake basket/",
        "mv pie basket",
        "mv pie basket/",
        "mv sandwich basket",
        "mv sandwich basket/",
        "mv grapes basket",
        "mv grapes basket/",
        "mv milk basket",
        "mv milk basket/"
    ]
    command = "blah"

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.other_commands:
            return True

    def check_command(self, line, current_dir):
        if line.strip() not in self.other_commands:
            hint = (
                '{{r:Use the command}} {{yb:' +
                self.other_commands[1] +
                '}} {{rn:to progress}}'
            )

        else:
            index = self.other_commands.index(line)
            if index % 2 == 0:
                # Remove the two elements
                # e.g. mv banana basket and mv banana basket/
                self.other_commands.pop(index)
                self.other_commands.pop(index)
            else:
                self.other_commands.pop(index - 1)
                self.other_commands.pop(index - 1)

            hint = '{{gb:Well done! Keep going}}'

        self.send_hint(hint)

    # Check that the basket folder contains the correct number of files?
    def check_output(self, line):
        basket_dir = os.path.join(HIDDEN_DIR, 'my-house/kitchen/basket')
        food_files = [
            f for f in os.listdir(basket_dir)
            if os.path.isfile(os.path.join(basket_dir, f))
        ]

        if len(food_files) > 3:
            return True
        else:
            return False

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Now move the basket to the {{yb:.hidden-shelter}}",

    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = [
        "mv basket ../../town/.hidden-shelter",
        "mv basket ../../town/.hidden-shelter/",
        "mv basket ~/town/.hidden-shelter",
        "mv basket ~/town/.hidden-shelter/",
    ]
    hints = [
        "{{r:Use the command}} {{yb:mv basket ~/town/.hidden-shelter}} "
        "to move the basket to the hidden-shelter"
    ]
    basket_file = os.path.join(HIDDEN_DIR, 'town', '.hidden-shelter', 'basket')

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

    # This doesn't currently do anything
    def check_output(self, line):
        return os.path.exists(self.basket_file)

    def next(self):
        Step6()


class Step6(StepTemplateMv):
    story = [
        "Finally, go back to the {{yb:.hidden-shelter}} using {{yb:cd}}"
    ]
    start_dir = "kitchen"
    end_dir = ".hidden-shelter"
    command = [
        "cd ../../town/.hidden-shelter/",
        "cd ../../town/.hidden-shelter",
        "cd ~/town/.hidden-shelter/",
        "cd ~/town/.hidden-shelter"
    ]
    hints = [
        "{{r:Use the command}} {{yb:cd ~/town/.hidden-shelter}} "
        "{{r:to get back to the hidden-shelter}}"
    ]

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        "{{wn:Talk to the people using}} {{yb:cat}} {{wn:and see how they "
        "react to the food}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    hints = [
        "Talk to everyone using {{yb:cat}}"
    ]
    allowed_commands = {
        "cat Edith": [
            "{{wb:Edith:}} You saved my little girl and my dog, and now "
            "you've saved us from starvation...how can I thank you?",
            "{{wb:Edith:}} You saved my little girl, and now you've saved "
            "us from starvation...how can I thank you?",
            "{{wb:Edith:}} Sniff...thank you.  I appreciate your kindness. "
            "I can't eat though, I miss my daughter too much...",
        ],
        "cat Eleanor": [
            "{{wb:Eleanor:}} Yummy! See, I told you doggy, someone would "
            "help us.",
            "{{wb:Eleanor:}} Oooh, food!  If only doggy was here...",
            ""
        ],
        "cat Edward": [
            "{{wb:Edward:}} Thank you!  I knew you would come through for us.",
            "{{wb:Edward:}} Thank you!  I knew you would come through for us.",
            "{{wb:Edward:}} Thank you!  I knew you would come through for us."
        ],
        "cat dog": [
            "{{wb:dog:}} \"Woof!\". \nThe dog seems very excited.",
            "",
            ""
        ]
    }

    def check_command(self, line, current_dir):
        # Decide which index to take for each option
        girl = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/Eleanor')
        dog = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/dog')

        if os.path.exists(girl):
            if os.path.exists(dog):
                index = 0
            else:
                index = 1
        else:
            index = 2

        if line.strip() in self.allowed_commands.keys():

            hint = self.allowed_commands[line][index]
            del self.allowed_commands[line]
            num_people = len(self.allowed_commands.keys()) - index

            if num_people == 0:
                self.send_hint(hint)
                return True

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
                "}} {{rn:to progress}}"
            )

        self.send_hint(hint)

    def next(self):
        pass
