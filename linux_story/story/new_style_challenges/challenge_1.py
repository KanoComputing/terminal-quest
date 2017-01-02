# challenge_1.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
import sys

from linux_story.IStep import IStep
from linux_story.dependencies import translate

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.new_terminals.terminal_ls import TerminalLs
from linux_story.sound_manager import SoundManager
from linux_story.helper_functions import wrap_in_box


class StepLs(IStep):
    TerminalClass = TerminalLs


# ----------------------------------------------------------------------------------------


class Step1(StepLs):
    story = [
        translate("{{wb:Alarm}}: {{Bb:\"Beep beep beep! Beep beep beep!\"}}"),
        translate("{{wb:Radio}}: {{Bb:\"Good Morning, this is the 9am news.\"\n"),
        translate("\"The town of Folderton has awoken to strange news. There have been reports of missing people and "
                  "damaged buildings across the town, with more stories coming in as we speak.\""),
        translate("\n\"Mayor Hubert has called an emergency town meeting and we'll keep you posted as it "
                  "happens...\"}}\n"),
        translate("It's time to get up sleepy head!\n "),
    ]  # TODO: " \ is a hack in this array to stop word wrap code screwing up and adding new lines in where it shouldn't

    story += wrap_in_box([
        translate("{{gb:New Spell:}} Type {{yb:ls}} and press"),
        translate("{{ob:Enter}} to {{lb:look around}}."),
    ])

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "ls"
    highlighted_commands = ["ls"]
    hints = [
        translate("{{rb:Type}} {{yb:ls}} {{rb:and press}} {{ob:Enter}} {{rb:to take a look around your bedroom.}}")
    ]

    last_step = True

    def _run_at_start(self):
        sound_manager = SoundManager()
        sound_manager.play_sound('alarm')

    def next(self):
        return 2, 1
