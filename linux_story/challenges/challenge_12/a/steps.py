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

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.challenges.challenge_11.terminals import TerminalMv
from linux_story.file_data import HIDDEN_DIR, copy_data
from linux_story.challenges.challenge_13.steps import Step1 as NextStep
from linux_story.helper_functions import play_sound


class StepTemplateMv(Step):
    challenge_number = 12

    def __init__(self):
        Step.__init__(self, TerminalMv)


# You lose the dog
class Step1(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{wn:Oh no!  I heard the sound of a bell.",
        "Check that my little girl is alright!}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"

    command = [
        "ls ..",
        "ls ../",
        "ls -a ..",
        "ls -a ../",
        "ls ~/town",
        "ls ~/town/",
        "ls -a ~/town",
        "ls -a ~/town/"
    ]

    hints = [
        "{{rn:Use the command}} {{yb:ls ..}} {{rn:to look in the lower "
        "directory}}"
    ]

    def next(self):
        Step2()


# Put dramatic music here?  Or loop some track
class Step2(StepTemplateMv):
    story = [
        "{{wn:The dog has disappeared!}}\n",
        # Ideally, make this font slightly smaller
        "{{wb:Eleanor:}} {{wn:Oh no!  Doggy gone!",
        "....am I next?}}\n",

        # Normal sized
        "{{wb:Edith:}} {{wn:Get my daughter back!}}"
    ]

    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
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
        "{{r:Use the command}} {{y:mv ../Eleanor .}}",
    ]
    counter = 0
    girl_file = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/Eleanor')

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            if 'cd' in line:
                print 'Ability to Change Directory has been blocked'
            return True

    def check_command(self, line, current_dir):
        # Need to check if the girl is in the correct directory

        # strip any spaces off the beginning and end
        line = line.strip()

        if os.path.exists(self.girl_file) and self.counter < 1:
            return True
        # We can't verify the girl has been moved correctly at this step
        elif line.strip() in self.command and self.counter == 1:
            return True
        elif self.counter == 1:
            return True
        else:
            self.show_hint(line, current_dir)
            return False

    def show_hint(self, line, current_dir):
        hint = (
            "{{rn:Quick!  Use}} {{yb:mv ../Eleanor .}} "
            "{{rn:to move the little girl back to safety}}"
        )
        self.counter += 1
        self.send_hint(hint)

    def next(self):
        # if girl is saved
        if os.path.exists(self.girl_file):
            Step3()

        # Else go to Step5b
        else:
            copy_data(12, 3, 'a')
            play_sound('bell')
            Step4()


# You save the little girl, but lose the dog.
class Step3(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{wn:Oh thank goodness I have you back safely.}}",
        "{{wb:Eleanor:}} {{wn:I lost my Doggie!!!}}",
        "{{wb:Edith:}} {{wn:I know I know, there's nothing we could do "
        "about that.}}",
        "{{wb:Edward:}} {{wn:Thank you so much for saving our little "
        "girl.}}\n",
        "{{gb:Well done for saving the little girl.}}",
        "Ask the people if there's anything else you can do to help."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = "cat Edward"
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} \"Thank you so much!  Eleanor, don't "
        "run outside again.\"",
        "cat Eleanor": "\n{{wb:Eleanor:}} \"Where has my dog gone?  Can you "
        "find him and bring him back?\""
    }
    hints = [
        "{{r:Edward looks like he has something to say.  Talk to him using "
        "{{yb:cat}}}}"
    ]

    def show_hint(self, line, current_dir):
        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            self.send_hint(hint)
        else:
            StepTemplateMv.show_hint(self, line, current_dir)

    # Change this so we can cat everyone and see how they respond
    def next(self):
        NextStep()


# You lose both the dog and the little girl.
class Step4(StepTemplateMv):
    story = [
        "{{wb:Edith:}} I heard a bell!",
        "Check on my little girl!"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "ls ../",
        "ls ..",
        "ls ~/town",
        "ls ~/town/"
    ]
    hints = [
        "{{r:Use the command}} {{yb:ls ..}} {{rn:to look back a directory}}"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "{{wb:Edith:}} My little girl has gone! How could you let her get "
        "taken away like that??",
        "{{wb:Edward:}}  Oh, this is awful\n",
        "{{rn:You}} {{rb:failed}} {{rn:at your mission.}}\n",

        # To simplify the game, you could have a game over screen here
        "Talk to the people to see if you can make up for this."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = "cat Edward"
    hints = [
        "{{r:Edward looks like he has something to ask.  Talk to him}}",
        "{{r:Use}} {{yb:cat Edward}} {{rn:to talk to Edward}}"
    ]
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} \"Don't talk to me.\""
    }
    last_step = True

    def show_hint(self, line, current_dir):
        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            self.send_hint(hint)
        else:
            StepTemplateMv.show_hint(self, line, current_dir)

    def next(self):
        # When you talk to the correct person
        NextStep()
