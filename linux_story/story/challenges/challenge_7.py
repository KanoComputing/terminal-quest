# challenge_7.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
import sys

from linux_story.story.tasks.TaskTownHall import TaskTownHall

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_8 import Step1 as NextChallengeStep


class StepTemplateCd(TerminalCd):
    challenge_number = 7


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        _("Have a {{lb:look around}} to see what's going on!")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = _("{{rb:To look around, use}} {{yb:ls}}")

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        _("Wow, there's so many people here. Find the {{bb:Mayor}} and {{lb:listen}} to what he has to say.")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "cat Mayor"
    hints = _("{{rb:Stuck? Type:}} {{yb:cat Mayor}}")

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        _("{{wb:Mayor:}} {{Bb:\"Calm down please! We have our best people looking into the disappearances, and we're hoping to have an explanation soon.\"}}\n"),
        _("Something strange is happening. Better check everyone is ok."),
        _("Type {{yb:cat}} to check on the people.")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    last_step = True

    task = TaskTownHall()

    def check_command(self):
        if self.task.passed(self.last_user_input):
            return True

        self.send_text(self.task.get_hint_text(self.last_user_input))

    def next(self):
        NextChallengeStep(self.xp)
