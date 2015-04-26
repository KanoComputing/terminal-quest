#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.Step import Step
from linux_story.step_helper_functions import (
    unblock_commands_with_cd_hint, unblock_commands_with_mkdir_hint,
    unblock_commands
)
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_22 import Step1 as NextChallengeStep


class StepTemplateMkdir(Step):
    challenge_number = 21

    def __init__(self, xp=''):
        Step.__init__(self, TerminalMkdir, xp)


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:Nice! You've build an igloo! You learned the new skill - mkdir!}}",
        "\nRuth: {{Bb:That's amazing!  Please help me build a shelter!",
        "Can we build it in the}} {{yb:barn}}, {{Bb:as then it'll be easier to "
        "move the animals inside.}}",
        "\n{{yb:Go back into the barn}}"
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/barn"
    commands = [
        "cd ../barn/",
        "cd ../barn",
        "cd ~/farm/barn",
        "cd ~/farm/barn/"
    ]
    hints = [
        "{{rb:Go back to the barn in one step by going back "
        "a directory first. Try using}} "
        "{{yb: cd ../barn}}"
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:Anyone can find the igloo though, "
        "can we make something that people can't find. Do you have "
        "any ideas how we can make a hidden shelter?}}",
        "\nTo make something hidden, you need to put a dot . in front of the "
        "name.",
        "Make a shelter called {{yb:.shelter}}. Remember the dot at the start!"
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    hint = [
        "{{rb:Make a shelter called}} {{yb:.shelter}}{{rb: - remember the dot at the start!}}"
    ]
    commands = [
        "mkdir .shelter"
    ]

    def block_command(self, line):
        return unblock_commands_with_mkdir_hint()

    def check_command(self, line, current_dir):
        # check files in the toolshed directory
        pass

    def next(self):
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        "Check it is properly hidden. Use {{yb:ls}} to "
        "see if it is visible.",
    ]

    commands = [
        "ls"
    ]

    def check_command(self, line, current_dir):
        line = line.strip()
        if line == "ls -a":
            self.send_hint(
                "{{rb:Use}} {{yb:ls}} {{rb:instead of}} {{yb:ls -a}} "
                "{{yb:to check that you can't see it.}}"
            )

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Now look around with {{yb:ls -a}} to check it actually exists!"
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls -a}} {{rb:to look around}}"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:Did you make something? That's amazing! "
        "...unfortunately I can't see it...please can you put me ",
        "and the animals inside?}}",
        "{{gb:Move everyone into the}} {{.shelter}} {{gb:one by one using}} "
        "{{yb:mv <name> .shelter}}"
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    all_commands = [
        "mv Trotter .shelter",
        "mv Trotter .shelter/",
        "mv Daisy .shelter",
        "mv Daisy .shelter/",
        "mv Cobweb .shelter",
        "mv Cobweb .shelter/"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.all_commands)

    def check_command(self, line, current_dir):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # strip any spaces off the beginning and end
        line = line.strip()

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = "\n{{gb:Well done for looking around.}}"
            self.send_text(hint)
            return False

        # check through list of commands
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

            if len(self.all_commands) == 1:
                hint += (
                    "\n{{gb:Well done! Move one more in the}}"
                    " {{yb:.shelter}}"
                )
            elif len(self.all_commands) > 0:
                hint += "\n{{gb:Well done! Move " + \
                    str(len(self.all_commands)) + \
                    " more.}}"
            else:
                hint += "\n{{gb:Press Enter to continue}}"

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        Step6()


class Step6(StepTemplateMkdir):
    story = [
        "Head into the {{yb:.shelter}} along with Ruth and the "
        "animals"
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn/.shelter"
    commands = [
        "cd .shelter",
        "cd .shelter/"
    ]

    def block_commands(self, line):
        unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step7()


class Step7(StepTemplateMkdir):
    story = [
        "Have a look around with {{yb:ls}} to check you moved everyone."
    ]
    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"
    commands = ["ls"]
    hints = ["Look around using {{yb:ls}}"]

    def next(self):
        NextChallengeStep(self.xp)
