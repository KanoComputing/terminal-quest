# challenge_27.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.challenges.challenge_28 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_bernard import \
    TerminalMkdirBernard, TerminalNanoBernard
from linux_story.helper_functions import wrap_in_box


class StepTemplateMkdir(TerminalMkdirBernard):
    challenge_number = 27


class StepTemplateNano(TerminalNanoBernard):
    challenge_number = 27


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
    story_dict = {
        "Eleanor": {
            "path": "~/town/east/shed-shop"
        }
    }
    eleanors_speech = (
        _("Eleanor: {{Bb:\"Achoo! This place is really dusty...*sniff*\"}}")
    )

    def next(self):
        Step2()


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

    eleanors_speech = \
        _("Eleanor: {{Bb:They taught us how to write at school. " +\
        "I don't think Bernard is very clever.}}")

    goal_nano_end_content = "echo \"Honk!\""
    goal_nano_filepath = "~/town/east/shed-shop/best-horn-in-the-world.sh"
    goal_nano_save_name = "best-horn-in-the-world.sh"

    # Overwrite the default behaviour for most of the steps - nano needs
    # slightly different behaviour.
    def check_command(self):
        if self.last_user_input == "cat Eleanor":
            self.send_text("\n" + self.eleanors_speech)
        else:
            return self.check_nano_input()

    def check_nano_content(self):
        return self.check_nano_content_default()

    def next(self):
        Step3()


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

    eleanors_speech = _("Eleanor: {{Bb:Will it be loud?}}")
    hints = [
        _("{{rb:Use}} {{yb:./best-horn-in-the-world.sh}} " +\
        "{{rb:to run the script.}}")
    ]

    def next(self):
        Step4()


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
        _("{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}}{{rb:,}} " +\
        "{{yb:echo 3}} {{rb:or}} {{yb:echo 4}}")
    ]

    eleanors_speech = \
        _("Eleanor: {{Bb:\"I have a question - does he have candy in his " +\
        "basement?\"}}")

    commands = [
        "echo 2"
    ]

    def check_command(self):
        if self.last_user_input == "echo 1":
            text = (
                _("\nBernard: {{Bb:\"Ah, trade secret. *wink*\"}}")
            )
            self.send_text(text)
        elif self.last_user_input == "echo 3":
            text = (
                _("\nBernard: {{Bb:\"Er, what? No, I wasn't planning " +\
                "on doing so. Why would I do that?\"}}")
            )
            self.send_text(text)
        elif self.last_user_input == "echo 4":
            text = (
                _("\nBernard: {{Bb:\"Oh ho ho ho, that's none of your business.\"}}")
            )
            self.send_text(text)
        else:
            return StepTemplateNano.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    print_text = [
        _("{{yb:\"What's the next big tool you want to create?\"}}")
    ]

    story = [
        _("Bernard: {{Bb:\"I want to know how the}} " +\
        "{{bb:private-section}} {{Bb:is locked " +\
        "in the}} {{bb:library}}{{Bb:, and then make a " +\
        "key to unlock it.\"}}"),

        _("\nEleanor: {{Bb:\"I guess the}} {{bb:librarian}} {{Bb:would have locked the " +\
        "private section.\"}}"),

        _("{{Bb:\"Maybe she can tell us how she did it? We should look for " +\
        "her.\"}}"),

        _("\n{{lb:Leave}} the {{bb:shed-shop}}.")
    ]

    hints = [
        _("{{rb:Use}} {{yb:cd}} {{rb:to leave the shed-shop.}}"),
        _("{{rb:Use}} {{yb:cd ..}} {{rb:to go}} {{lb:back}} {{rb:to town.}}"),
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east"
    eleanors_speech = \
        _("Eleanor: {{Bb:\"What do you think is hidden in the private-section?}}" +\
        "\n{{Bb:Maybe Bernard shouldn't see it...\"}}")
    last_step = True

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)
