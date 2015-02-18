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
from linux_story.challenges.challenge_4.terminals import TerminalCd

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.challenges.challenge_11.terminals import TerminalMv
from linux_story.challenges.challenge_12.steps import Step1 as NextStep
from linux_story.file_data import copy_data, HIDDEN_DIR
from linux_story.step_helper_functions import unblock_command_list


class StepTemplateCd(Step):
    challenge_number = 11

    def __init__(self):
        Step.__init__(self, TerminalCd)


class StepTemplateMv(Step):
    challenge_number = 11

    def __init__(self):
        Step.__init__(self, TerminalMv)


# The next few steps should be like the disappearing of people in the town
class Step1(StepTemplateCd):
    story = [
        "{{gb:Congratulations, you earned 30 XP!}}\n",
        "You see a group of people.",
        "They look quite thin and scared.",
        "Try talking to them."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = "cat Edward"

    # Use functions here
    command = "cat Edward"
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} {{Bb:\"You found us!  Edward, I told you "
        "to keep your voice down.\"}}",
        "cat Eleanor": "\n{{wb:Eleanor:}} {{Bb:\"My mummy is scared the bell will "
        "find us if we go outside.\"}}",
        "cat Edward": "\n{{wb:Edward:}} {{Bn:\"Oh hullo.  Can you help me?\"}}",
        "cat dog": "\n{{wb:dog:}} {{Bb:\"Woof woof!\"}}"
    }

    def show_hint(self, line, current_dir):
        line = line.strip()

        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            del self.all_commands[line]
            hint += "\n{{gb:Well done!  Talk to someone else.}}"
        else:
            hint = (
                "\n{{rb:Use}} {{yb:" +
                self.all_commands.keys()[0] +
                "}} {{rb:to progress}}"
            )

        self.send_hint(hint)

    def next(self):
        Step2()


# After we've heard some of the story from all the people
class Step2(StepTemplateMv):
    story = [
        "{{wb:Edward:}} {{Bb:\"Oh hullo.  Can you help me?\"",
        "\"I learnt this spell for moving items from"
        " one place to another.\"",
        "\"I've been trying to move this}} {{yb:apple}} {{Bb:into the}} "
        "{{yb:basket}}\"",
        "{{Bb:\"I was told the command was}} {{yb:mv apple basket/}}\"",
        "{{Bb:\"But I don't understand what that means.  Do I say it?\"}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "mv apple basket",
        "mv apple basket/"
    ]
    hints = [
        "{{gb:See if you can succeed where Edward failed. "
        "Try and}} {{yb:move}} {{gb:the}} {{yb:apple}} {{gb:into the}} "
        "{{yb:basket}}",
        "{{rb:Use the command}} {{yb:mv apple basket/}} {{rb:to}} "
        "{{yb:m}}{{rb:o}}{{yb:v}}{{rb:e the apple into the basket}}"
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "{{w:Check you have indeed moved the apple.  Look around in this "
        "directory}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Look in this directory to check you've moved the apple}}",
        "{{rb:Use}} {{yb:ls}} {{rb:to check the apple is not here}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "{{gb:Looking good, the apple isn't in this directory anymore}}",
        "{{wn:Now check the apple is in the basket}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "ls basket",
        "ls basket/",
        "ls -a basket",
        "ls -a basket/"
    ]
    hints = [
        "{{rb:Now look in the}} {{yb:basket}} {{rb:to check you've moved the "
        "apple in the basket}}",
        "{{rb:Use the}} {{yb:ls}} {{rb:command to look in the}} {{yb:basket}}",
        "{{rb:Use the command}} {{yb:ls basket}} {{rb:to progress}}"
    ]

    def next(self):
        Step5()


# After cat-ing the person again?
class Step5(StepTemplateMv):
    story = [
        "{{gb:Cool, the apple is now in the basket!}}",
        "\n{{wb:Edward:}} {{Bb:\"Hey, you did it!  What was I doing "
        "wrong?\"}}",
        "{{Bb:\"Can you move the apple back from the basket to here?\"}}\n",
        "You want to {{yb:move}} the {{yb:apple}} from the {{yb:basket}} to "
        "{{yb:.}} which represents your current position"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = "mv basket/apple ."
    hints = [
        "{{rb:Use the command}} {{yb:mv basket/apple .}} {{rb:to}} "
        "{{yb:m}}{{rb:o}}{{yb:v}}{{rb:e the apple from the basket to your "
        "current position.}}"
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def check_command(self, line, current_dir):
        if line.strip() == "mv basket/apple":
            hint = (
                "{{gb:Nearly!  However the full command is}} "
                "{{yb:mv basket/apple .}} {{gb:- don't forget the dot!}}"
            )
            self.send_hint(hint)
        else:
            return StepTemplateMv.check_command(self, line, current_dir)

    def next(self):
        copy_data(11, 6)
        Step6()


# Get three attempts to save the girl
class Step6(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{Bb:\"You should stop playing with that, that's the "
        "last of our food.\"}}",
        "{{Bb:\"Ah!  The dog ran outside!\"}}",
        "{{wb:Eleanor:}} {{Bb:\"Doggy!\"}}",
        "{{wb:Edith:}} {{Bb:\"No, honey!  Don't go outside\"}}",
        "\n{{wn:The little girl follows her dog and leaves the "
        ".hidden-shelter}}",
        "Look around to confirm this."
    ]

    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "ls", "ls -a"
    ]
    hints = [
        "{{rb:Look around using}} {{yb:ls}} {{rb:to confirm Eleanor ran "
        "outside}}"
    ]

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{Bb:\"No!!  Honey, come back!!\"}}",
        "{{Bb:\"You there, save my little girl!\"}}\n",
        "First, check to see that Eleanor is in the {{yb:town}} directory"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ""
    command = [
        "ls ..",
        "ls ../",
        "ls ~/town",
        "ls ~/town/"
    ]
    hints = [
        "{{rb:Look in the town directory by using either}} {{yb:ls ../}} "
        "{{rb:or}} {{yb:ls ~/town/}}"
    ]

    def next(self):
        # for now
        Step8()


class Step8(StepTemplateMv):
    story = [
        "Now {{yb:move}} {{wn:the girl from the}} {{yb:town}} {{wn:into}} "
        "{{yb:this directory}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden_shelter"
    command = [
        "mv ../Eleanor .",
        "mv ../Eleanor ./",
        "mv ~/town/Eleanor ~/town/.hidden-shelter",
        "mv ~/town/Eleanor ~/town/.hidden-shelter/",
        "mv ~/town/Eleanor .",
        "mv ~/town/Eleanor ./",
        "mv ../Eleanor ~/town/.hidden-shelter",
        "mv ../Eleanor ~/town/.hidden-shelter/",
    ]
    hints = [
        '{{rb:Move}} {{yb:Eleanor}} {{rb:from the previous directory}} '
        '{{yb:..}} {{rb:to}} {{yb:.}} '
        '{{rb:which represents this directory, using}} {{yb:mv}}',
        "{{rb:You need to move}} {{yb:Eleanor}} {{rb:from}} {{yb:../}} "
        "{{rb:to}} {{yb:.}}",
        "{{rb:Quick!  Use}} {{yb:mv ../Eleanor .}} "
        "{{rb:to move the little girl back to safety}}"
    ]
    last_step = True
    girl_file = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/Eleanor')

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def check_command(self, line, current_dir):

        # strip any spaces off the beginning and end
        line = line.strip()

        if os.path.exists(self.girl_file):
            return True

        else:
            self.show_hint(line, current_dir)
            return False

    def next(self):
        NextStep()
