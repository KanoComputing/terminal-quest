# challenge_24.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.new_style_challenges.CompanionMisc import StepTemplateMkdir


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        _("You walk down the narrow road, with {{bb:Eleanor}} dancing " +\
        "alongside, until you reach an open space in the " +\
        "{{bb:east}} part of town."),
        _("\n{{lb:Look around.}}")
    ]
    commands = [
        "ls",
        "ls -a"
    ]

    start_dir = "~/town/east"
    end_dir = "~/town/east"
    hints = [
        _("{{rb:Look around with}} {{yb:ls}}{{rb:.}}")
    ]
    deleted_items = ["~/town/Eleanor"]
    file_list = [{"path": "~/town/east/Eleanor"}]

    companion_speech = _("Eleanor: {{Bb:I can't see my parents anywhere...but there's a weird building there.}}")

    def next(self):
        return 24, 2


class Step2(StepTemplateMkdir):
    story = [
        _("You see a {{bb:shed-shop}}, {{bb:library}} and {{bb:restaurant}}."),
        _("\nEleanor: {{Bb:\"Hey, what is that shed-shop?\"}}\n"),
        _("{{Bb:\"Let's}} {{lb:go in}}{{Bb:!\"}}")
    ]

    start_dir = "~/town/east"
    end_dir = "~/town/east/shed-shop"
    hints = [
        _("{{rb:Use}} {{yb:cd shed-shop}} {{rb:to go in the shed-shop.}}")
    ]

    companion_speech = _("Eleanor: {{Bb:Do you think they sell candy?}}")

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 24, 3


# Duplicate of Step1, except that self.next is changed
class Step3(StepTemplateMkdir):
    # Have a sign with "the-best-shed-maker-in-town"

    story = [
        _("You both walk slowly into the shop."),
        _("It is dusty and significantly darker in here than outside."),
        _("{{bb:Eleanor}} looks like she needs to sneeze."),
        _("\n{{lb:Look around.}}")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    hints = [
        _("{{rb:Look around with}} {{yb:ls}}{{rb:.}}")
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    deleted_items = ["~/town/east/Eleanor"]
    file_list = [{"path": "~/town/east/shed-shop/Eleanor"}]
    companion_speech = _("Eleanor: {{Bb:Ah..ah...achoo!! It's so dusty in here!}}")

    def next(self):
        return 24, 4


class Step4(StepTemplateMkdir):

    story = [
        _("You see a man called {{bb:Bernard}}, a door and a couple of tools."),
        _("\nThe tools show up as {{gb:green}} in the Terminal."),
        _("\n{{lb:Listen}} to what {{bb:Bernard}} has to say.")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    hints = [
        _("{{rb:Use}} {{yb:cat Bernard}} {{rb:to see what Bernard has to say.}}")
    ]

    commands = [
        "cat Bernard"
    ]
    companion_speech = _("Eleanor: {{Bb:My}} {{lb:cat}} {{Bb:used to be a great listener, I'd tell her everything.}}")

    def next(self):
        return 25, 1
