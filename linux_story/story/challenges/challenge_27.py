# challenge_27.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.helper_functions import wrap_in_box
from linux_story.story.challenges.CompanionMisc import StepTemplateMkdir, StepTemplateNano


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        _("You are back in {{bb:Bernard}}'s place.\n"),
        _("{{lb:Listen}} to what {{bb:Bernard}} has to say.")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    hints = [
        _("{{rb:Use}} {{yb:cat Bernard}} {{rb:to interact with Bernard.}}")
    ]

    commands = [
        "cat Bernard"
    ]

    deleted_items = ["~/town/east/library/Eleanor"]
    file_list = [
        {
            "path": "~/town/east/shed-shop/Eleanor",
            "contents": get_story_file("Eleanor"),
            "type": "file"
        }
    ]
    companion_speech = (
        _("Eleanor: {{Bb:\"Achoo! This place is really dusty...*sniff*\"}}")
    )

    def next(self):
        return 27, 2


class Step2(StepTemplateNano):
    story = [
        _("Bernard: {{Bb:\"Hellooooo. You came back to fix my script!\"}}\n "),
    ]
    story += wrap_in_box([
        _("{{gb:New Spell}}: {{yb:nano}} followed by an"),
        _("object lets you {{lb:edit}} it"),
    ])
    story += [
        _("Let's try and use {{yb:nano best-horn-in-the-world.sh}} to edit it."),
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    commands = [
        "nano best-horn-in-the-world.sh"
    ]
    highlighted_commands = ['nano']

    hints = [
        _("{{rb:Use}} {{yb:nano best-horn-in-the-world}} " +\
        "{{rb:to edit the tool.}}")
    ]

    companion_speech = _("Eleanor: {{Bb:They taught us how to write at school. I don't think Bernard is very clever.}}")

    def _setup_nano(self):
        self._nano.set_goal_nano_save_name("best-horn-in-the-world.sh")
        self._nano.set_goal_nano_end_content("echo \"Honk!\"")
        self._nano.set_goal_nano_filepath("~/town/east/shed-shop/best-horn-in-the-world.sh")

    def check_command(self, line):
        if line == "cat Eleanor":
            self.send_hint("\n" + self.companion_speech)
        else:
            return self._nano.check_nano_input()

    def check_nano_contents(self):
        return self._nano.check_nano_content_default()

    def next(self):
        return 27, 3


class Step3(StepTemplateNano):
    story = [
        _("Now time to test your script!"),
        _("Use {{yb:./best-horn-in-the-world.sh}} to run it.")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    commands = [
        "./best-horn-in-the-world.sh"
    ]

    companion_speech = _("Eleanor: {{Bb:Will it be loud?}}")
    hints = [
        _("{{rb:Use}} {{yb:./best-horn-in-the-world.sh}} {{rb:to run the script.}}")
    ]

    def next(self):
        return 27, 4


class Step4(StepTemplateNano):
    # Allow the user to ask all the questions within the same Step?
    story = [
        _("{{gb:Congratulations, the script now prints \"Honk!\"}}"),

        _("\nBernard: {{Bb:\"The tool is working! Wonderful! " +\
        "Thank you so much!\"}}"),

        _("\nIt occurs to you that you haven't asked {{bb:Bernard}} much about " +\
        "himself."),

        _("What would you like to ask him?"),

        _("\n{{yb:1 \"How did you create your tools?\"}}"),

        _("{{yb:2: \"What's the next big tool you want to create?\"}}"),

        _("{{yb:3: \"Are you going into hiding now?\"}}"),

        _("{{yb:4: \"What's in your basement?\"}}"),

        _("\nUse {{yb:echo}} to ask him a question.")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    hints = [
        _("{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}}{{rb:,}} {{yb:echo 3}} {{rb:or}} {{yb:echo 4}}")
    ]

    companion_speech = _("Eleanor: {{Bb:\"I have a question - does he have candy in his basement?\"}}")

    commands = [
        "echo 2"
    ]

    def check_command(self, line):
        if line == "echo 1":
            text = (
                _("\nBernard: {{Bb:\"Ah, trade secret. *wink*\"}}")
            )
            self.send_hint(text)
        elif line == "echo 3":
            text = (
                _("\nBernard: {{Bb:\"Er, what? No, I wasn't planning " +\
                "on doing so. Why would I do that?\"}}")
            )
            self.send_hint(text)
        elif line == "echo 4":
            text = (
                _("\nBernard: {{Bb:\"Oh ho ho ho, that's none of your business.\"}}")
            )
            self.send_hint(text)
        else:
            return StepTemplateNano.check_command(self, line)

    def next(self):
        return 27, 5


class Step5(StepTemplateNano):
    print_text = [
        _("{{yb:\"What's the next big tool you want to create?\"}}")
    ]

    story = [
        _("Bernard: {{Bb:\"I want to know how the}} {{bb:private-section}} {{Bb:is locked " +\
        "in the}} {{bb:library}}{{Bb:, and then make a key to unlock it.\"}}"),

        _("\nEleanor: {{Bb:\"I guess the}} {{bb:librarian}} {{Bb:would have locked the private section.\"}}"),

        _("{{Bb:\"Maybe she can tell us how she did it? We should look for her.\"}}"),

        _("\n{{lb:Leave}} the {{bb:shed-shop}}.")
    ]

    hints = [
        _("{{rb:Use}} {{yb:cd}} {{rb:to leave the shed-shop.}}"),
        _("{{rb:Use}} {{yb:cd ..}} {{rb:to go}} {{lb:back}} {{rb:to town.}}"),
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east"
    companion_speech = \
        _("Eleanor: {{Bb:\"What do you think is hidden in the private-section?}}" +\
        "\n{{Bb:Maybe Bernard shouldn't see it...\"}}")

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 28, 1
