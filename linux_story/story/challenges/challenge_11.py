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
from linux_story.story.terminals.terminal_cd import TerminalCd

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_12 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_command_list
from linux_story.common import tq_file_system


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
        "You see a group of people and a dog.",
        "They all look quite thin and nervous.",
        "Try talking to them with {{yb:cat}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"

    # Use functions here
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} {{Bb:\"You found us!  Edward, I told "
        "you to keep your voice down.\"}}",
        "cat Eleanor": "\n{{wb:Eleanor:}} {{Bb:\"My mummy is scared the "
        "bell will find us if we go outside.\"}}",
        "cat Edward": "\n{{wb:Edward:}} {{Bb:\"I'm sorry Edith...but I "
        "don't think they mean any harm.  Maybe they could help us?\"}}",
        "cat dog": "\n{{wb:Dog:}} {{Bb:\"Woof woof!\"}}"
    }

    def check_command(self, line, current_dir):

        if not self.all_commands:
            hint = "\n{{gb:Press Enter to continue}}"
            return True

        # strip any spaces off the beginning and end
        line = line.strip()

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = "\n{{gb:Well done for looking around.}}"
            self.send_text(hint)
            return False

        # check through list of commands
        command_validated = False
        end_dir_validated = False
        self.hints = [
            "{{rb:Use}} {{yb:" + self.all_commands.keys()[0] + "}} "
            "{{rb:to progress}}"
        ]

        end_dir_validated = current_dir == self.end_dir

        # if the validation is included
        if line in self.all_commands.keys() and end_dir_validated:
            # Print hint from person
            hint = "\n" + self.all_commands[line]

            self.all_commands.pop(line, None)

            if len(self.all_commands) > 0:
                hint += "\n{{gb:Well done! Check on " + \
                    str(len(self.all_commands)) + \
                    " more.}}"
            else:
                command_validated = True
                hint += "\n{{gb:Press Enter to continue}}"

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        return command_validated and end_dir_validated

    def next(self):
        Step2()


# After we've heard some of the story from all the people
class Step2(StepTemplateMv):
    story = [
        "Edward looks like he has something he wants to say to you.\n",
        "{{wb:Edward:}} {{Bb:\"Hi there. Can you help me with something?\"",
        "\"I learnt this spell for moving items from"
        " one place to another.\"",
        "\"I've been trying to move this}} {{yb:apple}} {{Bb:into the}} "
        "{{yb:basket}}{{Bb:\"}}",
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
        "{{ob:See if you can succeed where Edward failed.}} "
        "{{ob:Use the command}} {{yb:mv apple basket/}} {{ob:to "
        "move the apple into the basket}}"
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
        "{{rb:Use}} {{yb:ls}} {{rb:to look around}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "{{gb:Looking good, the apple isn't in this directory anymore}}\n",
        "{{wn:Now check the apple is in the}} {{yb:basket}} {{wn:using}} "
        "{{yb:ls}}"
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
        "{{rb:Use the command}} {{yb:ls basket/}} {{rb:to look in the basket}}"
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
        "You want to move the apple from the {{yb:basket}} "
        "to your current position {{yb:.}}, so use {{yb:mv basket/apple .}}",
        "The {{yb:.}} is intentional!"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "mv basket/apple .",
        "mv basket/apple ./"
    ]
    hints = [
        "{{rb:Use the command}} {{yb:mv basket/apple .}} {{rb:to}} "
        "{{yb:m}}{{rb:o}}{{yb:v}}{{rb:e the apple from the basket to your "
        "current position.}}"
    ]
    story_dict = {
        "Eleanor": {
            "path": "~/town"
        },
        "dog": {
            "path": "~/town"
        }
    }

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
        self.move_girl_and_dog()
        Step6()


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
        "First, look for Eleanor outside with {{yb:ls ..}}",

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
        Step8()


class Step8(StepTemplateMv):
    story = [
        "Now move {{yb:Eleanor}} from the town outside {{yb:..}} to "
        "your current position {{yb:.}} "
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
        "{{rb:Quick!  Use}} {{yb:mv ../Eleanor .}} "
        "{{rb:to move the little girl back to safety}}"
    ]
    last_step = True
    girl_file = os.path.join(tq_file_system, 'town/.hidden-shelter/Eleanor')

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
