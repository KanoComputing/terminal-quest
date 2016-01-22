# challenge_8.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
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

from linux_story.gtk3.Storybook import OTHER_SLEEP
from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_9 import Step1 as NextChallengeStep
from linux_story.helper_functions import play_sound


class StepTemplateCd(TerminalCd):
    challenge_number = 8


class StepTemplateCdBell(StepTemplateCd):

    def __init__(self, story, xp=""):
        self.story = story

        t = threading.Thread(target=self.play_bell_delay)
        t.start()
        StepTemplateCd.__init__(self, xp)

    def play_bell_delay(self):
        delay = 0

        for text in self.story:
            if 'ding' in text.lower():
                break
            delay += len(text)

        delay *= OTHER_SLEEP * 1.3

        time.sleep(delay)
        play_sound('bell')


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):

    story = [
        "{{pb:Ding. Dong.}}\n",
        "It sounds like the bell you heard before.\n",
        "Use {{yb:ls}} to {{lb:look around}} again."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    deleted_items = ["~/town/grumpy-man"]

    def __init__(self, xp=""):
        play_sound("bell")
        StepTemplateCd.__init__(self, xp)

    def next(self):
        # This was the code we had originally. Did the bell ring properly?
        Step2()


class Step2(StepTemplateCdBell):

    story = [
        "{{wb:Little-boy:}} {{Bb:\"Oh no! That grumpy-man "
        "with the funny legs has gone!}} "
        "{{Bb:Did you hear the bell just before he vanished??\"}}",
        "{{wb:Young-girl:}} {{Bb:\"I'm scared...\"}}",
        "\n{{pb:Ding. Dong.}}\n",
        "{{wb:Young-girl:}} {{Bb:\"Oh! I heard it go again!\"}}",
        "\nTake a {{lb:look around}} you to check."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    deleted_items = ["~/town/little-boy"]

    def __init__(self):
        StepTemplateCdBell.__init__(self, self.story)

    def next(self):
        Step3()


class Step3(StepTemplateCdBell):

    story = [
        "{{wb:Young-girl:}} {{Bb:\"Wait, there was a}} {{bb:little-boy}} "
        "{{Bb:here...right?\"",
        "Every time that bell goes, someone disappears!}}",
        "{{wb:Mayor:}} {{Bb:\"Maybe they just decided to go home...?\"}}",
        "\n{{pb:Ding. Dong.}}\n",
        "{{lb:Look around.}}"
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    deleted_items = ["~/town/young-girl"]

    def __init__(self):
        StepTemplateCdBell.__init__(self, self.story)

    def next(self):
        Step4()


class Step4(StepTemplateCd):

    story = [
        "You are alone with the {{bb:Mayor}}.\n",
        "{{lb:Listen}} to what the {{bb:Mayor}} has to say."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "cat Mayor"
    hints = "{{rb:Use}} {{yb:cat Mayor}} {{rb:to talk to the Mayor.}}"

    def next(self):
        Step5()


class Step5(StepTemplateCdBell):

    story = [
        "{{wb:Mayor:}} {{Bb:\"Everyone...has disappeared??\"\n",
        "\"....I should head home now...\"}}",
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

    def __init__(self):
        StepTemplateCdBell.__init__(self, self.story)

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "Everyone has gone.",
        "Wait - there's a {{bb:note}} on the floor.\n",
        "Use {{yb:cat}} to read the {{bb:note}}."
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "cat note"
    hints = "{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}"
    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
