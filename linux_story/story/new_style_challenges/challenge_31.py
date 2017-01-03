# challenge_31.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.sound_manager import SoundManager
from linux_story.story.new_terminals.terminal_nano import TerminalNano


class StepTemplateNano(StepTemplate):
    TerminalClass = TerminalNano


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateNano):
    story = [
        _("You've arrived in the {{bb:shed-shop}}. {{lb:Look around.}}")
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    def next(self):
        return 31, 2


class Step2(StepTemplateNano):
    story = [
        _("Huh, you can't see {{bb:Bernard}} anywhere."),

        _("I wonder where he went.\n"),

        _("Maybe he's in his {{bb:basement}}? Let's {{lb:go}} down there.")
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop/basement"
    hints = [
        _("{{rb:Go into the basement with}} {{yb:cd basement}}")
    ]

    def check_command(self, line):
        if line == "cat Bernards-hat":
            self.send_hint(_("\nIs that Bernard\'s hat? Strange he left it behind..."))
        else:
            return StepTemplateNano.check_command(self, line)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 31, 3


class Step3(StepTemplateNano):
    story = [
        _("You walked into {{bb:Bernard}}'s basement. {{lb:Look around.}}")
    ]
    start_dir = "~/town/east/shed-shop/basement"
    end_dir = "~/town/east/shed-shop/basement"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Look around with}} {{yb:ls}}{{rb:.}}")
    ]

    def _run_at_start(self):
        sound_manager = SoundManager()
        sound_manager.play_sound('steps')

    def next(self):
        return 31, 4


class Step4(StepTemplateNano):
    story = [
        _("You see what looks like another tool and a couple of diaries.\n"),
        _("Shall we {{lb:examine}} them?")
    ]
    start_dir = "~/town/east/shed-shop/basement"
    end_dir = "~/town/east/shed-shop/basement"
    commands = [
        "cat bernards-diary-1",
        "cat bernards-diary-2",
        "cat photocopier.sh"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat}} {{rb:to examine the objects around you.}}")
    ]

    def check_command(self, line):
        if line in self.commands:
            self.commands.remove(line)

            if not self.commands:
                text = _("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")
                self.send_hint(text)
            else:
                text = _("\n{{gb:Well done! Look at the other objects.}}")
                self.send_hint(text)

        elif not line and not self.commands:
            return True

        else:
            return StepTemplateNano.check_command(self, line)

    def next(self):
        return 32, 1
