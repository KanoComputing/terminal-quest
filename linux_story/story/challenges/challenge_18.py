#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.step_helper_functions import (
    unblock_cd_commands
)
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_19 import Step1 as NextStep


class StepTemplate(TerminalEcho):
    challenge_number = 18


class Step1(StepTemplate):
    story = [
        "Woah! You spoke aloud into the empty room!",
        "{{gb:You learnt the new skill echo!}}",
        "This command can probably be used to talk to people.",

        "\nNow let's head to ~ to find that farm!",
        "Type {{yb:cd}} by itself to go to the Windy Road {{lb:~}}"
    ]

    hints = [
        "{{rb:Use}} {{yb:cd}} {{rb:by itself to go to}} {{lb:~}}"
    ]

    start_dir = "~/my-house/parents-room"
    end_dir = "~"

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplate):
    story = [
        "You are back on the windy road, which stretches endlessly in both "
        "directions. {{lb:Look around.}}"
    ]
    hints = [
        "{{rb:Look around with}} {{yb:ls}}{{rb:.}}"
    ]

    commands = [
        "ls",
        "ls -a"
    ]
    start_dir = '~'
    end_dir = '~'

    def next(self):
        Step3()


class Step3(StepTemplate):
    story = [
        "You notice a small remote farm in the distance.",
        "{{lb:Let's go}} to the {{lb:farm}}."
    ]

    start_dir = "~"
    end_dir = "~/farm"
    hints = [
        "{{rb:Use}} {{yb:cd farm/}} {{rb:to head to the farm.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


class Step4(StepTemplate):
    story = [
        "{{lb:Look around.}}"
    ]

    commands = "ls"
    start_dir = "~/farm"
    end_dir = "~/farm"
    hints = ["{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"]

    def next(self):
        Step5()


class Step5(StepTemplate):
    story = [
        "You are in a farm, with a {{bb:barn}}, a {{bb:farmhouse}} and "
        "a large {{bb:toolshed}} in sight.",
        "The land is well tended and weed free, so there must "
        "be people about here.",
        "{{lb:Look around}} and see if you can "
        "find someone to talk to."
    ]
    start_dir = "~/farm"
    end_dir = "~/farm"
    counter = 0

    def finished_challenge(self, line):
        output = self.check_output(self.last_cmd_output)
        if not output:
            # If Ruth not in output, check if command is ls
            self.check_command()

        return output

    def output_condition(self, output):
        if 'Ruth' in output:
            return True

        return False

    def check_command(self):
        if self.last_user_input == 'ls' or 'ls ' in self.last_user_input:
            self.counter += 1

            if self.counter >= 3:
                self.send_text(
                    "\n{{rb:Use}} {{yb:ls barn}} {{rb:to look in the barn.}}"
                )
            if self.counter == 2:
                self.send_text(
                    "\n{{rb:Have you looked in the}} {{lb:barn}} {{rb:yet?}}"
                )
            elif self.counter == 1:
                self.send_text(
                    "\n{{rb:There is no one here. You should look somewhere "
                    "else.}}"
                )

        else:
            self.send_text("\n{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")

    def block_command(self):
        if "mv" in self.last_user_input:
            return True

    def next(self):
        Step6()


class Step6(StepTemplate):

    story = [
        "In the barn, you see a woman tending some animals.",
        "{{lb:Walk}} into the {{lb:barn}} so you can have a closer look."
    ]

    start_dir = "~/farm"
    end_dir = "~/farm/barn"
    hints = [
        "{{rb:Use}} {{yb:cd barn/}} {{rb:to walk into the barn.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step7()


class Step7(StepTemplate):

    story = [
        # "In the barn, you see a woman tending some animals.",
        # "You walk into the barn to have a closer look.",
        "{{lb:Examine}} everyone in the barn using "
        "the {{lb:cat}} command."
    ]

    # what is this?
    last_challenge = True

    all_commands = {
        "cat Ruth": "Ruth: {{Bb:Ah! Who are you?!}}",
        "cat Cobweb": "Cobweb: {{Bb:Neiiigh.}}",
        "cat Trotter": "Trotter: {{Bb:Oink Oink.}}",
        "cat Daisy": "Daisy: {{Bb:Mooooooooo.}}"
    }

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    last_step = True

    hints = [
        "{{rb:If you've forgotten who's in the barn, use}} "
        "{{yb:ls}} {{rb:to remind yourself.}}"
    ]

    # TODO: move this into step_helper_functions, used a few too
    # many times outside.
    def check_command(self):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if self.last_user_input == 'ls':
            hint = "\n{{gb:Well done for looking around.}}"
            self.send_text(hint)
            return False

        # check through list of commands
        end_dir_validated = False
        end_dir_validated = self.current_path == self.end_dir

        # if the validation is included
        if self.last_user_input in self.all_commands.keys() and \
                end_dir_validated:

            # Print hint from person
            hint = "\n" + self.all_commands[self.last_user_input]

            self.all_commands.pop(self.last_user_input, None)

            if len(self.all_commands) == 1:
                hint += (
                    "\n{{gb:Well done! Have a look at one more.}}"
                )
            elif len(self.all_commands) > 0:
                hint += "\n{{gb:Well done! Look at " + \
                    str(len(self.all_commands)) + \
                    " more.}}"
            else:
                hint += "\n{{gb:Press Enter to continue.}}"

            self.send_text(hint)

        else:
            if not self.hints:
                self.hints = [
                    "{{rb:Use}} {{yb:" + self.all_commands.keys()[0] + "}} "
                    "{{rb:to progress.}}"
                ]
            self.send_hint()
            self.hints.pop()

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        NextStep(self.xp)
