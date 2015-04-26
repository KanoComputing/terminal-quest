#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
from linux_story.Step import Step
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_19 import Step1 as NextChallengeStep
from linux_story.common import tq_file_system


class StepTemplate(Step):
    challenge_number = 18

    def __init__(self, xp=""):
        Step.__init__(self, TerminalEcho, xp)


class Step1(StepTemplate):
    story = [
        "{{gb:Congratulations, you learnt the new skill echo!}}",
        "\n Woah! It makes you talk!",
        "This command can probably be used to talk to people.",
        "Move this command into your chest for safe keeping."
    ]
    hints = [
        "{{rb:Move the}} {{yb:mv}} {{rb:command into your}} {{yb:chest}} "
        "{{rb:in your}} {{yb:room}}",
        "{{rb:An easy way to do it is to}} {{yb:mv ECHO}} {{rb:from}} "
        "{{yb:.safe}} {{rb:to}} {{yb:../my-room/.chest}}",
        "{{rb:Use}} {{yb:mv .safe/ECHO ../my-room/.chest/}}"
    ]
    commands = [
        "mv .safe/ECHO ../my-room/.chest/",
        "mv .safe/ECHO ../my-room/.chest",
        "mv .safe/ECHO ~/my-house/my-room/.chest/",
        "mv .safe/ECHO ~/my-house/my-room/.chest"
    ]
    start_dir = "~/my-house/parents-room"

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def check_output(self, output):
        # This is run after the command has been run, so can check for the
        # existance of a file now

        echo_note_path = os.path.join(tq_file_system, 'my-house/my-room/.chest/ECHO')
        if os.path.exists(echo_note_path):
            return True

        return False

    def next(self):
        Step2()


class Step2(StepTemplate):
    story = [
        "Nice work! Let's head to ~ to find that farm!",
        "Type {{yb:cd}} by itself to go to {{yb:~}}"
    ]

    hint = [
        "Use {{yb:cd}} by itself to go to {{yb:~}}"
    ]

    commands = [
        "cd",
        "cd ~"
        "cd ~/"
    ]

    start_dir = "~/my-house/parents-room"
    end_dir = "~"
    last_step = True

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
        "{{rb:Look around with}} {{yb:ls}}"
    ]

    commands = "ls"
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
        "cd farm/"
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step5()


class Step5(StepTemplate):
    story = [
        "Look around."
    ]

    command = "ls"
    start_dir = "~/farm"
    end_dir = "~/farm"

    def next(self):
        Step6()


class Step6(StepTemplate):
    story = [
        "You are in a farm, with a {{bb:barn}}, a {{bb:farmhouse}} and "
        "a large {{bb:toolshed}} in sight.",
        "The land is well tended and weed free, so there must"
        " be people about here.  See if you can find someone to "
        "talk to."
    ]
    start_dir = "farm"

    def check_output(self, output):
        if not output:
            return False

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
        "In the barn, you see a woman called {{yb:Ruth}}",
        "You should talk to her and see if she knows what's going on."
    ]

    last_challenge = True

    command = "cat Ruth"
    hints = [
        "{{rb:Use}} {{yb:cat Ruth}} {{rb:to see what "
        "she has to say.}}"
    ]

    start_dir = "~/farm/barn"

    # TODO: why does this need to be specified here?
    end_dir = "~/farm/barn"

    def check_command(self, line, current_dir):
        return_value = StepTemplate.check_command(self, line, current_dir)
        return return_value

    def next(self):
        NextChallengeStep(self.xp)
