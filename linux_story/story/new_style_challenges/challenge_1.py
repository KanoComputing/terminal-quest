# challenge_1.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.StepTemplate import StepTemplate
from linux_story.story.new_terminals.terminal_ls import TerminalLs
from linux_story.sound_manager import SoundManager
from linux_story.helper_functions import wrap_in_box


class StepLs(StepTemplate):
    TerminalClass = TerminalLs


# ----------------------------------------------------------------------------------------


class Step1(StepLs):
    story = [
        _("{{wb:Alarm}}: {{Bb:\"Beep beep beep! Beep beep beep!\"}}"),
        _("{{wb:Radio}}: {{Bb:\"Good Morning, this is the 9am news.\"\n"),
        _("\"The town of Folderton has awoken to strange news. There have been reports of missing people and "
            "damaged buildings across the town, with more stories coming in as we speak.\""),
        _("\n\"Mayor Hubert has called an emergency town meeting and we'll keep you posted as it "
            "happens...\"}}\n"),
        _("It's time to get up sleepy head!\n "),
    ]  # TODO: " \ is a hack in this array to stop word wrap code screwing up and adding new lines in where it shouldn't

    story += wrap_in_box([
        _("{{gb:New Spell:}} Type {{yb:ls}} and press"),
        _("{{ob:Enter}} to {{lb:look around}}."),
    ])

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "ls"
    highlighted_commands = ["ls"]
    hints = [
        _("{{rb:Type}} {{yb:ls}} {{rb:and press}} {{ob:Enter}} {{rb:to take a look around your bedroom.}}")
    ]

    def _run_at_start(self):
        sound_manager = SoundManager()
        sound_manager.play_sound('alarm')

    def next(self):
        return 2, 1
