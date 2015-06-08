#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.step_helper_functions import (
    unblock_commands, unblock_commands_with_cd_hint
)
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_19 import Step1 as NextChallengeStep


class StepTemplate(TerminalEcho):
    challenge_number = 18


class Step1(StepTemplate):
    story = [
        "{{gb:Congratulations, you learnt the new skill echo!}}",
        "\nWoah! You spoke aloud into the empty room!",
        "This command can probably be used to talk to people.",
        "Move this command into your chest for safe keeping."
    ]
    hints = [
        "{{rb:An easy way to do it is to move}} {{lb:ECHO}} {{rb:from}} "
        "{{lb:.safe}} {{rb:to}} {{lb:../my-room/.chest}}{{rb:.}}",
        "{{rb:Use}} {{yb:mv .safe/ECHO ../my-room/.chest/}}{{rb:. "
        "Remember you can use TAB to speed up your typing.}}"
    ]
    commands = [
        "mv .safe/ECHO ../my-room/.chest/",
        "mv .safe/ECHO ../my-room/.chest",
        "mv .safe/ECHO ~/my-house/my-room/.chest/",
        "mv .safe/ECHO ~/my-house/my-room/.chest"
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplate):
    story = [
        "{{gb:Nice work!}} Let's head to ~ to find that farm!",
        "Type {{yb:cd}} by itself to go to the Windy Road {{lb:~}}"
    ]

    hints = [
        "{{rb:Use}} {{yb:cd}} {{rb:by itself to go to}} {{lb:~}}"
    ]

    commands = [
        "cd",
        "cd ~",
        "cd ~/"
    ]

    start_dir = "~/my-house/parents-room"
    end_dir = "~"

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step3()


class Step3(StepTemplate):
    story = [
        "You are back on the windy road, which stretches endlessly in both "
        "directions.  Look around."
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
        Step4()


class Step4(StepTemplate):
    story = [
        "You notice a small remote farm in the distance.",
        "Let's go that way."
    ]

    start_dir = "~"
    end_dir = "~/farm"
    commands = [
        "cd farm",
        "cd farm/",
        "cd ~/farm",
        "cd ~/farm/"
    ]
    hints = [
        "{{rb:Use}} {{yb:cd farm/}} {{rb:to head to the farm.}}"
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step5()


class Step5(StepTemplate):
    story = [
        "Look around."
    ]

    commands = "ls"
    start_dir = "~/farm"
    end_dir = "~/farm"
    hints = ["{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"]

    def next(self):
        Step6()


class Step6(StepTemplate):
    story = [
        "You are in a farm, with a {{bb:barn}}, a {{bb:farmhouse}} and "
        "a large {{bb:toolshed}} in sight.",
        "The land is well tended and weed free, so there must "
        "be people about here.  See if you can find someone to "
        "talk to."
    ]
    start_dir = "~/farm"
    end_dir = "~/farm"

    def finished_challenge(self, line, current_dir):
        return self.check_output(self.last_cmd_output)

    def output_condition(self, output):
        if 'Ruth' in output:
            return True

        return False

    def block_command(self, line):
        if "mv" in line:
            return True

    def next(self):
        Step7()


class Step7(StepTemplate):

    story = [
        "In the barn, you see a woman tending some animals.",
        "Take a closer look at everyone in the barn using "
        "the {{yb:cat}} command."
    ]

    # what is this?
    last_challenge = True

    all_commands = {
        "cat Ruth": "Ruth: {{Bb:Ah! Who are you?!}}",
        "cat Cobweb": "Cobweb: {{Bb:Neiiigh}}",
        "cat Trotter": "Trotter: {{Bb:Oink Oink}}",
        "cat Daisy": "Daisy: {{Bb:Mooooooooo}}"
    }

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    last_step = True

    # TODO: move this into step_helper_functions, used a few too
    # many times outside.
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
                    "\n{{gb:Well done! Have a look at one more}}"
                )
            elif len(self.all_commands) > 0:
                hint += "\n{{gb:Well done! Look at " + \
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
        NextChallengeStep(self.xp)
