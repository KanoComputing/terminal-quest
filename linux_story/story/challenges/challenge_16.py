# challenge_16.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.story.terminals.terminal_mv import TerminalMv


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        _("There is an old antique {{bb:.chest}} hidden under your bed, which you don't remember seeing before.\n"),
        _("You walk into {{bb:my-room}} to have a closer look.\n"),
        _("{{lb:Peer inside}} the {{bb:.chest}} and see what it contains.")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    commands = [
        'ls .chest',
        'ls .chest/',
        'ls -a .chest',
        'ls -a .chest/',
        'ls .chest/ -a',
        'ls .chest -a'
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls .chest}} {{rb:to look inside the .chest}}")
    ]

    def next(self):
        return 16, 2


class Step2(StepTemplateMv):
    story = [
        _("There are some scrolls, similar to what you found in the {{bb:.hidden-shelter}}. "
          "They could contain more powerful commands.\n"),
        _("Use {{yb:cat}} to {{lb:read}} one of the scrolls.\n")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    commands = [
        'cat .chest/LS',
        'cat .chest/CAT',
        'cat .chest/CD'
    ]

    hints = [
        _("{{rb:Use}} {{yb:cat .chest/LS}} {{rb:to read the LS scroll.}}")
    ]

    def next(self):
        return 16, 3


class Step3(StepTemplateMv):
    story = [
        _("I wonder if there's anything else hidden in this {{lb:.chest}}?"),
        _("Have a {{lb:closer look}} for some more items.")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    hints = [
        _("{{rb:Use}} {{yb:ls -a .chest}} {{rb:to see if there are any hidden items in the chest.}}")
    ]

    commands = [
        "ls -a .chest",
        "ls -a .chest/",
        'ls .chest/ -a',
        'ls .chest -a'
    ]

    def next(self):
        return 16, 4


class Step4(StepTemplateMv):
    story = [
        _("You suddenly notice a tiny stained {{lb:.note}}, scrumpled in the corner of the {{lb:.chest}}."),
        _("What does it say?\n")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    hints = [
        _("{{rb:Use}} {{yb:cat .chest/.note}} {{rb:to read the}} {{lb:.note}}{{rb:.}}")
    ]

    commands = [
        "cat .chest/.note"
    ]

    def next(self):
        return 17, 1
