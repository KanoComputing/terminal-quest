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
from linux_story.challenges.challenge_12.steps import Step1 as NextStep


class StepTemplateCd(Step):
    challenge_number = 10

    def __init__(self):
        Step.__init__(self, TerminalCd)


class StepTemplateMv(Step):
    challenge_number = 10

    def __init__(self):
        Step.__init__(self, TerminalMv)


# The next few steps should be like the disappearing of people in the town
class Step1(StepTemplateCd):
    story = [
        "You see a group of people.",
        "They look a quite thin and unkempt.",
        "Try talking to them."
    ]
    start_dir = "town"
    end_dir = ".hidyhole"
    command = ""
    hints = [
        "{{r:Use}} {{yb:cat}} {{r:to talk to one of people}}"
    ]

    def next(self):
        Step2()


# After we've heard some of the story from all the people
class Step2(StepTemplateMv):
    story = [
        "I learnt this spell for moving items from one place to another.",
        "I've been trying to move this {{yapple}} into the {{bbasket}}",
        "I was told the command was {{ymv apple basket}}",
        "But I don't understand what that means.  Do I say it?"
    ]
    start_dir = ".hidyhole"
    end_dir = ".hidyhole"
    command = [
        "mv apple basket",
        "mv apple basket/"
    ]
    hints = [
        "{{r:Use the command}} {{yb:mv apple basket}} to {{yb:m}}o{{yb:v}}e "
        "the apple into the basket"
    ]

    def next(self):
        Step3()


# After cat-ing the person again?
class Step3(StepTemplateMv):
    story = [
        "{{wb:Edward:}} Hey, you did it!",
        "{{w:What was I doing wrong?}}",
        "Hey, can you move the apple back from the basket to here?",
        "You want to move the apple from the basket to your current position, "
        "represented by ."
    ]
    start_dir = ".hidyhole"
    end_dir = ".hidyhole"
    command = "mv basket/apple ."
    hints = [
        "{{r:Use the command}} {{yb:mv basket/apple .}} to "
        "{{yb:m}}o{{yb:v}}e the apple from the basket to your current position"
    ]

    def next(self):
        Step4()


# Get three attempts to save the girl
class Step4(StepTemplateMv):
    story = [
        "Graham:  You should stop playing with that, that's the last of "
        "our food..."
        "Edith: {{w:Ah!  My cat ran outside!}}",
        "Little girl: {{w:Kitty!}}",
        "Edith: {{w:No, honey!  Don't go outside}}",
        "The little girl follows her cat and leaves the {{yb:.hidyhole}}",
        "Edith: {{w:No!!  Honey, come back!!}}",
        "{{w:You there, save my little girl!}}\n",
        "You need to move the little girl back to this directory."
    ]
    start_dir = ".hidyhole"
    end_dir = ".hidyhole"
    command = "mv ../little-girl ."
    hints = [
        "{{r:Use the command}} {{y:mv ../little-girl .}}"
    ]

    def next(self):
        # if girl is saved
        Step5a()
        # Else go to Step5b


# Thanks you for saving the little girl
class Step5a(StepTemplateMv):
    story = [
        "Edith: Thank you for saving her!",
        "Little girl: Kitty!",
        "Edith: Can you save her kitty too?  I'm worried something will "
        "happen to it if it stays outside"
    ]
    start_dir = ".hidyhole"
    end_dir = ".hidyhole"
    command = ""
    hints = [
        "{{r:Use the command}} {{y:mv ../cat .}}"
    ]

    def next(self):
        Step6a


# Save both the cat and the little girl
class Step6a(StepTemplateMv):
    story = [
        "Little girl: Yay, kitty!",
        "Cat: Meow.",
        "Edith: Oh thank goodness you got them both back.",
        "I was wrong about you. You're clearly a good person.",
        "Talk to the others and see if there's anything else you can do to"
        "help"
    ]
    start_dir = ".hidyhole"
    end_dir = ".hidyhole"
    command = ""
    hints = [
        "{{r:Use the command}} {{y:cat}} {{r:to see if you can help "
        "the others}}"
    ]

    def next(self):
        NextStep()
        # If you do the command correctly, save the cat


# You lose the cat
class Step5b(StepTemplateMv):
    story = [
        # Make this text smaller
        "Girl:  Oh no!  my cat has disappeared!",
        "Girl:  ....am I next?",
        # Normal sized
        "Edith: Get her back!"
    ]
    start_dir = ".hidyhole"
    end_dir = ".hidyhole"
    command = ""
    hints = [
        "{{r:Use the command}} {{y:mv ../little-girl .}}"
    ]

    def next(self):
        # If
        Step6b()


# You save the little girl, but lose the cat.
class Step6b(StepTemplateMv):
    story = [
        "Edith: Oh thank goodness I have you back safely.",
        "Girl:  I lost my kitty!!!",
        "Edith:  I know I know, there's nothing we could do about that."
        "Alice:  I'm glad you could save the little girl, even if we lost the "
        "cat.\n",
        "Ask the people if there's anything else you can do"
    ]
    start_dir = ".hidyhole"
    end_dir = ".hidyhole"
    command = ""
    hints = [
        "{{r:Use the command}} {{y:mv ../cat .}}"
    ]

    def next(self):
        NextStep()


# You lose both the cat and the little girl.
class Step6c(StepTemplateMv):
    story = [
        "Edith: My little girl! How could you let her get taken away like "
        "that??",
        "Alice: Oh no, that poor girl!  Who knows what's happened to her.",
        "Edward:  Oh, this is awful\n",
        "Talk to people to see if there's anything you can do anything else "
        "to help"
    ]
    start_dir = ".hidyhole"
    end_dir = ".hidyhole"
    command = ""
    hints = [
        "{{r:Use the command}} {{y:mv ../cat .}}"
    ]

    def next(self):
        # When you talk to the correct person
        NextStep()
