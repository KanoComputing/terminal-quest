#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys
import time
import threading

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.Step import Step
from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_9 import Step1 as NextChallengeStep
from linux_story.helper_functions import play_sound


class StepTemplateCd(Step):
    challenge_number = 8

    def __init__(self, xp=""):
        Step.__init__(self, TerminalCd, xp)


class StepTemplateCdBell(StepTemplateCd):

    def play_bell_delay(self):
        time.sleep(3)
        play_sound('bell')

    def run(self):
        t = threading.Thread(target=self.play_bell_delay)
        t.start()
        StepTemplateCd.run(self)


class Step1(StepTemplateCd):

    story = [
        "{{pb:Ding. Dong.}}\n",
        "It's that bell again? I wonder what it means.",
        "Use {{yb:ls}} to slook around again."
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "{{r:To look around, use}} {{yb:ls}}"

    story_dict = {
        "grumpy-man": {
            "exists": False
        }
    }

    def next(self):
        # This was the code we had originally.  Did the bell ring properly?
        Step2()


class Step2(StepTemplateCdBell):

    story = [
        "{{wb:Little-boy:}} {{Bb:Oh no!  Did you see that man with the funny legs earlier? "
        "He's gone! Disappeared!}}",
        "{{wb:Little-boy:}} {{Bb:Did you hear the bell just before he vanished??}}",
        "{{wb:Young-girl:}} {{Bb:I'm scared...}}",
        "\n{{pb:Ding. Dong.}}\n",
        "{{wb:Young-girl:}} {{Bb:Did you hear it? It rung again! I wonder if someone has disappeared this time?}}",
        "\nTake a look around you to check."
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "{{rb:To look around, use}} {{yb:ls}}"
    story_dict = {
        "little-boy": {
            "exists": False
        }
    }

    def run(self):
        StepTemplateCdBell.run(self)

    def next(self):
        Step3()


class Step3(StepTemplateCdBell):

    story = [
        "{{wb:Young-girl:}} {{Bb:Wait, there was a little boy here...right?",
        "Everytime that bell goes, someone disappears!}}",
        "{{wb:Mayor:}} {{Bb:It's fine, settle down everybody. Maybe they just decided to go home...?}}",
        "\n{{pb:Ding. Dong.}}\n",
        "Look around."
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "{{r:To look around, use}} {{yb:ls}}"
    story_dict = {
        "young-girl": {
            "exists": False
        }
    }

    def run(self):
        # copy_data(8, 5)
        StepTemplateCdBell.run(self)

    def next(self):
        Step4()


class Step4(StepTemplateCd):

    story = [
        "You are alone with the Mayor.",
        "Talk to the Mayor"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "cat Mayor"
    hints = "{{r:Use}} {{yb:cat Mayor}} {{r:to talk to the Mayor}}"

    def next(self):
        Step5()


class Step5(StepTemplateCdBell):

    story = [
        "{{wb:Mayor:}} {{Bb:\"Everyone ... has disappeared??\"",
        "....I need to go, you should get home and be safe!}}",
        "\n{{pb:Ding. Dong.}}\n"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "{{r:To look around, use}} {{yb:ls}}"
    story_dict = {
        "Mayor": {
            "exists": False
        },
        "note_town": {
            "name": "note",
            "path": "~/town"
        }
    }

    def run(self):
        StepTemplateCdBell.run(self)

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "Everyone has gone.",
        "Wait - there's another note on the floor.",
        "Use {{yb:cat}} to read the note."
    ]
    start_dir = "town"
    end_dir = "town"
    command = "cat note"
    hints = "{{rb:To read the note, use}} {{yb:cat note}}"
    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
