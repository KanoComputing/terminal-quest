# challenge_22.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.IStep import IStep
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.new_terminals.terminal_mkdir import TerminalMkdir


class StepTemplateMkdir(IStep):
    TerminalClass = TerminalMkdir


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        _("{{gb:Well done, it looks like everyone is here!}}"),
        _("\nRuth: {{Bb:\"Thank you so much!\"}}"),
        _("{{Bb:\"We'll stay in here to keep safe. I'm so grateful for everything " +\
        "you've done.\"}}"),
        _("\nUse {{yb:cat}} to check that the animals are happy in here.")
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"

    commands = [
        "cat Daisy",
        "cat Trotter",
        "cat Cobweb"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat}} {{rb:to examine an animal, e.g.}} {{yb:cat Daisy}}{{rb:.}}")
    ]

    deleted_items = [
        "~/town/.hidden-shelter/basket",
        "~/town/.hidden-shelter/apple"
    ]

    def next(self):
        return 22, 2


class Step2(StepTemplateMkdir):
    story = [
        _("{{pb:Ding. Dong.}}\n"),
        _("Ruth: {{Bb:\"What?? I heard a bell! What does that mean?\"}}"),
        _("Quick! {{lb:Look around}} and see if anyone is missing.")
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Look around with}} {{yb:ls}}{{rb:.}}")
    ]

    deleted_items = [
        "~/town/.hidden-shelter/Edith"
    ]

    def next(self):
        return 22, 3


class Step3(StepTemplateMkdir):

    story = [
        _("It appears that everyone is still here..."),
        _("{{pb:Ding. Dong.}}\n"),
        _("Ruth: {{Bb:\"I heard it again! Is that the sound you heard when my husband went missing?\"\n}}"),
        _("Have another quick {{lb:look around}}.")
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Look around with}} {{yb:ls}}{{rb:.}}")
    ]
    deleted_items = [
        "~/town/.hidden-shelter/Edward"
    ]

    def next(self):
        return 22, 4


# TODO: FIX THIS STEP
class Step4(StepTemplateMkdir):
    story = [
        _("Ruth: {{Bb:\"It's alright. We're all safe, everyone's still here. " +\
        "I wonder why it's ringing?\"}}"),
        _("Perhaps we should investigate that sound. Who else do we " +\
        "know?"),
        _("Maybe you should check back on the family in the " +\
        "{{bb:.hidden-shelter}} and talk to them with your new found voice."),
        "",
        _("Start heading back to the {{bb:.hidden-shelter}} using {{yb:cd}}.")
    ]

    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/town/.hidden-shelter"

    hints = [
        _("{{rb:We can go directly to the}} {{bb:.hidden-shelter}} " +\
        "{{rb:using}} {{yb:cd ~/town/.hidden-shelter}}")
    ]

    # Remove the dog
    deleted_items = [
        "~/town/.hidden-shelter/dog"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def check_command(self, line):
        # If the command passes, then print a nice hint.
        if line.startswith("cd") and not self.get_command_blocked() and not self.get_fake_path() == self.end_dir:
            hint = _("\n{{gb:You travel back to tilde}}")
            self.send_hint(hint)
        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 22, 5


class Step5(StepTemplateMkdir):
    story = [
        _("Have a {{lb:look around}}.")
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    def next(self):
        return 23, 1
