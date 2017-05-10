# challenge_15.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        _("You get the nagging feeling that you're missing something."),
        _("What was the command that helped you find the hidden shelter?\n"),
        _("Use it to have a {{lb:closer look around}}.\n")
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls -a}} {{rb:to look more closely around you.}}")
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
        return 15, 2


class Step2(StepTemplateMv):
    story = [
        _("What's that? There's {{bb:.tiny-chest}} in the corner of the shelter"),
        _("Have a {{lb:look inside}} the {{bb:.tiny-chest}}.")
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls .tiny-chest}} {{rb:to look inside}}")
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
        return 15, 3


class Step3(StepTemplateMv):
    story = [
        _("You see a special looking scroll with a stamp that says {{bb:MV}}"),
        _("{{lb:Read}} what it says.")
    ]

    hints = [
        _("{{rb:Use}} {{yb:cat .tiny-chest/MV}} {{rb:to read the MV parchment}}")
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "cat .tiny-chest/MV"
    ]

    def next(self):
        return 15, 4


class Step4(StepTemplateMv):
    story = [

        _("{{wb:Edward:}} {{Bb:\"Hey, that's our .tiny-chest. We use it to keep things safe. "),
        _("That MV command is how I found out about moving objects with mv."),
        _("It's probably more useful to you, please take it as a thank you for saving us.\"}}"),
        "",
        _("\nMaybe you should go back to {{bb:my-house}} to look for more hidden items."),
        _("To quickly go back home, use {{yb:cd ~/my-house}}\n")
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/my-house"
    commands = [
        'cd ~/my-house/',
        'cd ~/my-house'
    ]
    hints = [
        _("{{rb:No shortcuts! Use}} {{yb:cd ~/my-house}} {{rb:to get back to your house in one step.}}")
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 15, 5


class Step5(StepTemplateMv):
    story = [
        _("Let's see if we can find anything hidden around here!"),
        _("Where do you think any hidden things could be?\n"),
        _("Try {{lb:looking closely}} in {{bb:my-room}} first.")
    ]

    start_dir = '~/my-house'

    hints = [
        _("{{rb:Stuck? Have a look in}} {{yb:my-room}}{{rb:.}}"),
        _("{{rb:Use}} {{yb:ls -a my-room}} {{rb:to look for hidden files in}} {{lb:my-room}}{{rb:.}}")
    ]

    def check_output(self, output):
        # Need to check that .chest is shown in the output of the command
        if not output:
            return False

        if '.chest' in output:
            return True

        return False

    def next(self):
        return 16, 1
