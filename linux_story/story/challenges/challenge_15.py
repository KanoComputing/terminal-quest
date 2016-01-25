# challenge_15.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_16 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateMv(TerminalMv):
    challenge_number = 15


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        "You get the nagging feeling you're missing something.",
        "What was that spell that helped you find this place?",
        "Use it to have a {{lb:closer look around}}.\n"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls -a}} {{rb:to look more closely around you.}}"
    ]

    story_dict = {
        "CAT, LS, CD, .note": {
            "path": "~/my-house/my-room/.chest"
        }
    }

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls -a"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "What's that! There's {{bb:.tiny-chest}} in the corner of the shelter",
        "Have a {{lb:look inside}} the {{bb:.tiny-chest}}."
    ]

    hints = [
        "{{rb:Use}} {{yb:ls .tiny-chest}} {{rb:to look inside}}"
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls .tiny-chest",
        "ls .tiny-chest/",
        "ls -a .tiny-chest",
        "ls -a .tiny-chest/"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "You see a scroll of parchment inside, with a stamp on it saying "
        "{{bb:MV}}.",
        "{{lb:Read}} what it says."
    ]

    hints = [
        "{{rb:Use}} {{yb:cat .tiny-chest/MV}} {{rb:to read the MV parchment}}"
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "cat .tiny-chest/MV"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "{{wb:Edward:}} {{Bb:\"Hey, that's our .tiny-chest We "
        "use it to keep our possessions safe. ",
        "I learnt about how to move objects from that}} {{Bb:MV}} "
        "{{Bb:parchment.",
        "It's probably of more use to you, please take it with my thanks.\"}}",
        "\nMaybe you should go back to {{bb:my-house}} to look for more "
        "hidden items.",
        "To quickly go back home, use {{yb:cd ~/my-house}}\n"
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/my-house"
    commands = [
        'cd ~/my-house/',
        'cd ~/my-house'
    ]
    hints = [
        '{{rb:No shortcuts! Use}} {{yb:cd ~/my-house}} '
        '{{rb:to get back to your house in one step.}}'
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Let's see if we can find anything hidden around here!",
        "Where do you think any hidden things could be?\n",
        "Try {{lb:looking closely}} in {{bb:my-room}} first."
    ]

    start_dir = '~/my-house'

    hints = [
        "{{rb:Stuck? Have a look in}} {{yb:my-room}}{{rb:.}}",
        "{{rb:Use}} {{yb:ls -a my-room}} {{rb:to look for hidden files in}} "
        "{{lb:my-room}}{{rb:.}}"
    ]

    last_step = True

    def check_output(self, output):
        # Need to check that .chest is shown in the output of the command
        if not output:
            return False

        if '.chest' in output:
            return True

        return False

    def next(self):
        NextStep(self.xp)
