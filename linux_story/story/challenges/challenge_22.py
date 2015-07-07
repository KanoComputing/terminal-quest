#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.helper_functions import play_sound
from linux_story.story.challenges.challenge_23 import Step1 as NextStep


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 22


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:Well done, it looks like everyone is here!}}",
        "\nRuth: {{Bb:Thank you so much!}}",
        "{{Bb:We'll stay in here to keep safe.  I'm so grateful to everything "
        "you've done.}}",
        "\nUse {{lb:cat}} to check that the animals are happy in here."
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"

    commands = [
        "cat Daisy",
        "cat Trotter",
        "cat Cobweb"
    ]
    hints = [
        "{{rb:Use}} {{lb:cat}} {{rb:to examine an animal, e.g.}} "
        "{{yb:cat Daisy}}{{rb:.}}"
    ]

    # Remove all the food
    deleted_items = [
        "~/town/.hidden-shelter/basket",
        "~/town/.hidden-shelter/apple"
    ]

    def next(self):
        play_sound("bell")
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "{{pb:Ding. Dong.}}",
        "Ruth: {{Bb:What?? I heard a bell!  What does that mean?}}",
        "\nQuick! {{lb:Look around}} and see if anyone is missing."
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Look around with}} {{yb:ls}}{{rb:.}}"
    ]

    # Remove Edith
    deleted_items = [
        "~/town/.hidden-shelter/Edith"
    ]

    def next(self):
        play_sound("bell")
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        "It appears that everyone is still here...",
        "\n{{pb:Ding. Dong.}}",
        "\nRuth: {{Bb:I heard it again!  Is that the sound you heard when "
        "my husband went missing?}}",
        "Have another quick {{lb:look around}}."
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Look around with}} {{yb:ls}}{{rb:.}}"
    ]
    # Remove Edward
    deleted_items = [
        "~/town/.hidden-shelter/Edward"
    ]

    def next(self):
        play_sound("bell")
        Step4()


# TODO: FIX THIS STEP
class Step4(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:It's alright. We're all safe, everyone's still here. "
        "I wonder why it's ringing?}}",
        "\nPerhaps we should investigate that sound.  Who else do we "
        "know?",
        "Maybe you should check back on the family in the "
        "{{lb:.hidden-shelter}} and talk to them with your new found voice.",

        "\nStart heading back to the {{lb:.hidden-shelter}} using {{lb:cd}}."
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/town/.hidden-shelter"

    hints = [
        "{{rb:We can go directly to the}} {{lb:.hidden-shelter}} "
        "{{rb:using}} {{yb:cd ~/town/.hidden-shelter/}}"
    ]

    # Remove the dog
    deleted_items = [
        "~/town/.hidden-shelter/dog"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def check_command(self):
        # If the command passes, then print a nice hint.
        if self.last_user_input.startswith("cd") and \
                not self.get_command_blocked() and \
                not self.current_path == self.end_dir:
            hint = "\n{{gb:Well done! Keep going!}}"
            self.send_text(hint)
        else:
            return StepTemplateMkdir.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Have a {{lb:look around}}."
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
