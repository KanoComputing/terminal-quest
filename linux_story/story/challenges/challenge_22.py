# challenge_22.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import time
import threading

from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.helper_functions import play_sound
from linux_story.story.challenges.challenge_23 import Step1 as NextStep
from linux_story.gtk3.Storybook import OTHER_SLEEP


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 22


class StepTemplateMkdirBell(StepTemplateMkdir):

    def __init__(self, story, xp=""):
        self.story = story

        t = threading.Thread(target=self.play_bell_delay)
        t.start()
        StepTemplateMkdir.__init__(self, xp)

    def play_bell_delay(self):
        delay = 0

        for text in self.story:
            if 'ding' in text.lower():
                break
            delay += len(text)

        delay *= OTHER_SLEEP * 1.4

        time.sleep(delay)
        play_sound('bell')


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:Well done, it looks like everyone is here!}}",
        "\nRuth: {{Bb:\"Thank you so much!\"}}",
        "{{Bb:\"We'll stay in here to keep safe. I'm so grateful for everything "
        "you've done.\"}}",
        "\nUse {{yb:cat}} to check that the animals are happy in here."
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"

    commands = [
        "cat Daisy",
        "cat Trotter",
        "cat Cobweb"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat}} {{rb:to examine an animal, e.g.}} "
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
        "{{pb:Ding. Dong.}}\n",
        "Ruth: {{Bb:\"What?? I heard a bell! What does that mean?\"}}",
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
        Step3()


class Step3(StepTemplateMkdirBell):

    story = [
        "It appears that everyone is still here...",
        "\n{{pb:Ding. Dong.}}\n",
        "\nRuth: {{Bb:\"I heard it again! Is that the sound you heard when "
        "my husband went missing?\"\n}}",
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

    def __init__(self):
        StepTemplateMkdirBell.__init__(self, self.story)

    def next(self):
        Step4()


# TODO: FIX THIS STEP
class Step4(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:\"It's alright. We're all safe, everyone's still here. "
        "I wonder why it's ringing?\"}}",
        "\nPerhaps we should investigate that sound. Who else do we "
        "know?",
        "Maybe you should check back on the family in the "
        "{{bb:.hidden-shelter}} and talk to them with your new found voice.",

        "\nStart heading back to the {{bb:.hidden-shelter}} using {{yb:cd}}."
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/town/.hidden-shelter"

    hints = [
        "{{rb:We can go directly to the}} {{bb:.hidden-shelter}} "
        "{{rb:using}} {{yb:cd ~/town/.hidden-shelter}}"
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
            hint = "\n{{gb:You travel back to tilde}}"
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
