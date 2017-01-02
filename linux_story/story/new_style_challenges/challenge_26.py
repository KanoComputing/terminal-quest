# challenge_26.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.new_style_challenges.CompanionMisc import StepTemplateMkdir
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_cd_commands


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        _("You are back in town. {{bb:Eleanor}} waves her arms and points at a building in the distance."),
        _("\n{{lb:Look around}} to see where {{bb:Eleanor}} is pointing.")
    ]

    start_dir = "~/town/east"
    end_dir = "~/town/east"

    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    commands = [
        "ls",
        "ls -a"
    ]

    deleted_items = ["~/town/east/shed-shop/Eleanor"]
    file_list = [
        {
            "path": "~/town/east/Eleanor",
            "contents": get_story_file("Eleanor"),
            "type": "file"
        }
    ]
    companion_speech = _("Eleanor: {{Bb:The library is over there!}}")

    def next(self):
        return 26, 2


class Step2(StepTemplateMkdir):
    story = [
        _("You see the {{bb:library}} ahead."),
        _("Eleanor: {{Bb:\"There it is! The}} {{bb:library}} " +\
        "{{Bb:is right there! Let's}} {{lb:go inside.}}{{Bb:\"}}")
    ]

    start_dir = "~/town/east"
    end_dir = "~/town/east/library"

    hints = [
        _("{{rb:Use}} {{yb:cd library}} {{rb:to go inside the library.}}")
    ]
    companion_speech = _("Eleanor: {{Bb:I love the library! Let's go inside!}}")

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 26, 3


class Step3(StepTemplateMkdir):
    story = [
        _("{{bb:Eleanor}} skips into the {{bb:library}}, while you follow her.\n"),
        _("{{lb:Look around}} the {{bb:library}}.")
    ]

    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"

    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    deleted_items = ["~/town/east/Eleanor"]
    file_list = [
        {
            "path": "~/town/east/library/Eleanor",
            "contents": get_story_file("Eleanor")
        }
    ]
    companion_speech = _("Eleanor: {{Bb:It's all echo-y-y-y-y..}}")

    def next(self):
        return 26, 4


class Step4(StepTemplateMkdir):
    story = [
        _("You're in a corridor leading to two clearly " +\
        "labelled doors. " +\
        "One has the sign {{bb:public-section}}, the other " +\
        "{{bb:private-section}}.\n"),

        _("Eleanor: {{Bb:\"There used to be a librarian here."),

        _("She would tell me off for trying to look in the}} " +\
        "{{bb:private-section}}."),

        _("{{Bb:What do you think is in there? Let's try and}} " +\
        "{{lb:look inside}}{{Bb:.\"}}")
    ]

    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"

    commands = [
        "ls private-section/",
        "ls private-section"
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls private-section/}} {{rb:to look in the " +\
        "private-section of the library.}}")
    ]
    companion_speech = _("Eleanor: {{Bb:What's in the private-section?}}")

    def next(self):
        return 26, 5


class Step5(StepTemplateMkdir):

    story = [
        _("Eleanor: {{Bb:\"I guess the private-section is locked to outsiders...\""),

        _("\"Let's see if we can find something useful in the}} " +\
        "{{bb:public section.}}{{Bb:\"}}"),

        _("\nUse {{lb:ls}} to look in the {{bb:public-section}}.")
    ]

    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"
    commands = [
        "ls public-section",
        "ls public-section/",
        "ls -a public-section",
        "ls -a public-section/"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look in the public section.}}"),
        _("{{rb:Use}} {{yb:ls public-section}} {{rb:to look in the public-" +\
        "section.}}")
    ]
    companion_speech = _("Eleanor: {{Bb:What's in the public-section?}}")

    def next(self):
        return 26, 6


class Step6(StepTemplateMkdir):
    story = [
        _("Eleanor: {{Bb:\"Wow, all the commands have disappeared."),
        _("I wonder if people have been stealing them?\"\n}}"),

        _("{{Bb:\"What is that}} {{lb:NANO}} {{Bb:paper?\"}}\n"),
        _("{{Bb:\"Let's}} {{lb:examine}} {{Bb:it.\"}}")
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"
    commands = [
        "cat public-section/NANO"
    ]
    hints = [
        _("{{rb:Examine the NANO script with}} {{yb:cat public-section/NANO}}")
    ]
    companion_speech = (
        _("Eleanor: {{Bb:The library should probably have introduced late " +\
        "fees.}}")
    )

    def next(self):
        return 26, 7


class Step7(StepTemplateMkdir):
    story = [
        _("Eleanor: {{Bb:\"So nano allows you to edit files?}}"),

        _("{{Bb:Maybe we could use this to fix that}} " +\
        "{{yb:best-horn-in-the-world.sh}} {{Bb:script?\"}}\n"),

        _("{{Bb:\"Let's}} {{lb:head back}} {{Bb:to the}} {{bb:shed-shop}}{{Bb:.\"}}")
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/shed-shop"
    companion_speech = (
        _("Eleanor: {{Bb:...do we have to go and see creepy Bernard again?}}")
    )

    path_hints = {
        "~/town/east/library": {
            "blocked": _("\n{{rb:Use}} {{yb:cd ../}} {{rb:to go back.}}")
        },
        "~/town/east": {
            "not_blocked": _("\n{{gb:Now go into the}} {{bb:shed-shop}}{{gb:.}}"),
            "blocked": _("\n{{rb:Use}} {{yb:cd shed-shop/}} {{rb:to go into the shed-shop.}}")
        }
    }

    def check_command(self, line):
        if self.get_fake_path() == self.end_dir:
            return True
        elif "cd" in line and not self.get_command_blocked():
            hint = self.path_hints[self.get_fake_path()]["not_blocked"]
        else:
            hint = self.path_hints[self.get_fake_path()]["blocked"]

        self.send_hint(hint)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 27, 1
