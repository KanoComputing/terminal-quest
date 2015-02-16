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
from linux_story.challenges.challenge_4.terminals import TerminalCd

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.challenges.challenge_11.terminals import TerminalMv
from linux_story.challenges.challenge_12.a.steps import Step1 as LoseDogStep
from linux_story.challenges.challenge_12.b.steps import Step1 as SaveGirlStep
from linux_story.file_data import copy_data, HIDDEN_DIR
from linux_story.helper_functions import play_sound


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
        "cat Edith": "\n{{wb:Edith:}} \"You found us!  Edward, I told you "
        "to keep your voice down.\"",
        "cat Eleanor": "\n{{wb:Eleanor:}} \"My mummy is scared the bell will "
        "find us if we go outside.\"",
        "cat Edward": "\n{{wb:Edward:}} \"Oh hullo.  Can you help me?\"",
        "cat dog": "\n{{wb:dog:}} \"Woof woof!\""
    }

    def show_hint(self, line, current_dir):
        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            del self.all_commands[line]
            hint += "\n{{gb:Well done!  Talk to someone else.}}"
        else:
            hint = (
                "\n{{rn:Use}} {{yb:" +
                self.all_commands.keys()[0] +
                "}} {{rn:to progress}}"
            )

        self.send_hint(hint)

    def next(self):
        Step2()


# After we've heard some of the story from all the people
class Step2(StepTemplateMv):
    story = [
        "{{wb:Edward:}} {{wn:\"Oh hullo.  Can you help me?\"",
        "\"I learnt this spell for moving items from"
        " one place to another.\"",
        "\"I've been trying to move this}} {{yb:apple}} {{wn:into the}} "
        "{{yb:basket}}\"",
        "{{wn:\"I was told the command was}} {{yb:mv apple basket/}}\"",
        "{{wn:\"But I don't understand what that means.  Do I say it?\"}}"
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
        "{{r:Use the command}} {{yb:mv apple basket/}} {{rn:to}} "
        "{{yb:m}}{{rn:o}}{{yb:v}}{{rn:e the apple into the basket}}"
    ]

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

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
        "{{r:Look in this directory to check you've moved the apple}}",
        "{{r:Use}} {{yb:ls}} {{r:to check the apple is not here}}"
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
        "{{r:Now look in the}} {{yb:basket}} {{rn:to check you've moved the "
        "apple in the basket}}",
        "{{r:Use the}} {{yb:ls}} {{rn:command to look in the}} {{yb:basket}}",
        "{{r:Use the command}} {{yb:ls basket}} {{rn:to progress}}"
    ]

    def next(self):
        Step5()


# After cat-ing the person again?
class Step5(StepTemplateMv):
    story = [
        "{{gb:Cool, the apple is now in the basket!}}",
        "\n{{wb:Edward:}} {{wn:\"Hey, you did it!  What was I doing "
        "wrong?\"}}",
        "\"Can you move the apple back from the basket to here?\"\n",
        "You want to {{yb:move}} the {{yb:apple}} from the {{yb:basket}} to "
        "{{yb:.}} which represents your current position"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = "mv basket/apple ."
    hints = [
        "{{r:Use the command}} {{yb:mv basket/apple .}} {{rn:to}} "
        "{{yb:m}}{{rn:o}}{{yb:v}}{{rn:e the apple from the basket to your "
        "current position.}}"
    ]

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

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
        "{{wb:Edith:}} {{wn:\"You should stop playing with that, that's the "
        "last of our food.\"}}",
        "{{wn:\"Ah!  The dog ran outside!\"}}",
        "{{wb:Eleanor:}} {{wn:\"Doggy!\"}}",
        "{{wb:Edith:}} {{wn:\"No, honey!  Don't go outside\"}}",
        "\nThe little girl follows her dog and leaves the "
        ".hidden-shelter",
        "Look around to confirm this."
    ]

    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "ls", "ls -a"
    ]
    hints = [
        "{{r:Look around using}} {{yb:ls}} {{rn:to confirm Eleanor ran "
        "outside}}"
    ]

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{wn:\"No!!  Honey, come back!!\"}}",
        "{{wn:\"You there, save my little girl!\"}}\n",
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
        "{{rn:Look in the town directory by using either}} {{yb:ls ../}} "
        "{{rn:or}} {{yb:ls ~/town/}}"
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
        '{{rn:Move}} {{yb:Eleanor}} {{rn:from the previous directory}} '
        '{{yb:..}} {{rn:to}} {{yb:.}} '
        '{{rn:which represents this directory, using}} {{yb:mv}}',
        "{{rn:You need to move}} {{yb:Eleanor}} {{rn:from}} {{yb:../}} "
        "{{rn:to}} {{yb:.}}",
        "{{rn:Quick!  Use}} {{yb:mv ../Eleanor .}} "
        "{{rn:to move the little girl back to safety}}"
    ]
    counter = 0
    last_step = True
    girl_file = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/Eleanor')

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            if 'cd' in line:
                print 'Ability to Change Directory has been blocked'
            return True

    def check_command(self, line, current_dir):

        # strip any spaces off the beginning and end
        line = line.strip()

        if os.path.exists(self.girl_file) and self.counter < 3:
            return True

        # We can't verify the girl has been moved correctly at this step
        elif line.strip() in self.command and self.counter == 3:
            return True

        elif self.counter == 3:
            return True

        else:
            self.show_hint(line, current_dir)
            return False

    def show_hint(self, line, current_dir):
        self.counter += 1
        StepTemplateMv.show_hint(self, line, current_dir)

    def next(self):
        # if girl is saved
        if os.path.exists(self.girl_file):
            SaveGirlStep()

        # Else go to Step5b
        else:
            play_sound('bell')
            copy_data(12, 1, 'a')
            LoseDogStep()
