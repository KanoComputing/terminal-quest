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

from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_9 import Step1 as NextChallengeStep
from linux_story.helper_functions import play_sound


class StepTemplateCd(TerminalCd):
    challenge_number = 8


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
        "It sounds like the bell you heard before.",
        "Use {{yb:ls}} to look around again."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    deleted_items = ["~/town/grumpy-man"]

    def __init__(self, xp=""):
        play_sound('bell')
        StepTemplateCd.__init__(self, xp)

    def next(self):
        # This was the code we had originally.  Did the bell ring properly?
        Step2()


class Step2(StepTemplateCdBell):

    story = [
        "{{wb:Little-boy:}} {{Bb:Oh no! That}} {{lb:grumpy-man}} "
        "{{Bb:with the funny legs has gone!}} "
        "{{Bb:Did you hear the bell just before he vanished??}}",
        "{{wb:Young-girl:}} {{Bb:I'm scared...}}",
        "\n{{pb:Ding. Dong.}}\n",
        "{{wb:Young-girl:}} {{Bb:Oh!  I heard it go again!}}",
        "\nTake a look around you to check."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    deleted_items = ["~/town/little-boy"]

    def run(self):
        StepTemplateCdBell.run(self)

    def next(self):
        Step3()


class Step3(StepTemplateCdBell):

    story = [
        "{{wb:Young-girl:}} {{Bb:Wait, there was a}} {{lb:little-boy}} "
        "{{Bb:here...right?",
        "Every time that bell goes, someone disappears!}}",
        "{{wb:Mayor:}} {{Bb:Maybe they just decided to go home...?}}",
        "\n{{pb:Ding. Dong.}}\n",
        "Look around."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    deleted_items = ["~/town/young-girl"]

    def run(self):
        StepTemplateCdBell.run(self)

    def next(self):
        Step4()


class Step4(StepTemplateCd):

    story = [
        "You are alone with the Mayor.",
        "Talk to the Mayor."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "cat Mayor"
    hints = "{{rb:Use}} {{yb:cat Mayor}} {{rb:to talk to the Mayor.}}"

    def next(self):
        Step5()


class Step5(StepTemplateCdBell):

    story = [
        "{{wb:Mayor:}} {{Bb:\"Everyone...has disappeared??\"",
        "....I should head home now...}}",
        "\n{{pb:Ding. Dong.}}\n"
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    deleted_items = ["~/town/Mayor"]
    story_dict = {
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
        "Wait - there's a note on the floor.",
        "Use {{lb:cat}} to read the note."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "cat note"
    hints = "{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}"
    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
