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


class StepTemplateMkdir(TerminalMkdirBernard):
    challenge_number = 27


class StepTemplateNano(TerminalNanoBernard):
    challenge_number = 27


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        "You are back in {{bb:Bernard}}'s place.\n",
        "{{lb:Listen}} to what {{bb:Bernard}} has to say."
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    hints = [
        "{{rb:Use}} {{yb:cat Bernard}} {{rb:to interact with Bernard.}}"
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
        "Eleanor: {{Bb:\"Achoo! This place is really dusty...*sniff*\"}}"
    )

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Bernard: {{Bb:\"Hellooooo. You came back to fix my script!\"}}\n ",
        "+--------------------------------------------------------+",
        "| {{gb:New Spell}}: {{yb:nano}} followed by an object lets you {{lb:edit}} it | " \
        "+--------------------------------------------------------+ ",
        "\nLet's try and use {{yb:nano best-horn-in-the-world.sh}} to edit it.",
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    commands = [
        "nano best-horn-in-the-world.sh"
    ]
    highlighted_commands = ['nano']

    hints = [
        "{{rb:Use}} {{yb:nano best-horn-in-the-world}} "
        "{{rb:to edit the tool.}}"
    ]

    eleanors_speech = (
        "Eleanor: {{Bb:They taught us how to write at school. "
        "I don't think Bernard is very clever.}}"
    )

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
        "Now time to test your script!",
        "Use {{yb:./best-horn-in-the-world.sh}} to run it."
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    commands = [
        "./best-horn-in-the-world.sh"
    ]

    eleanors_speech = (
        "Eleanor: {{Bb:Will it be loud?}}"
    )
    hints = [
        "{{rb:Use}} {{yb:./best-horn-in-the-world.sh}} "
        "{{rb:to run the script.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    # Allow the user to ask all the questions within the same Step?
    story = [
        "{{gb:Congratulations, the script now prints \"Honk!\"}}",

        "\nBernard: {{Bb:\"The tool is working! Wonderful! "
        "Thank you so much!\"}}",

        "\nIt occurs to you that you haven't asked {{bb:Bernard}} much about "
        "himself.",

        "What would you like to ask him?",

        "\n{{yb:1 \"How did you create your tools?\"}}",

        "{{yb:2: \"What's the next big tool you want to create?\"}}",

        "{{yb:3: \"Are you going into hiding now?\"}}",

        "{{yb:4: \"What's in your basement?\"}}",

        "\nUse {{yb:echo}} to ask him a question."
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    hints = [
        "{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}}{{rb:,}} "
        "{{yb:echo 3}} {{rb:or}} {{yb:echo 4}}"
    ]

    eleanors_speech = (
        "Eleanor: {{Bb:\"I have a question - does he have candy in his "
        "basement?\"}}"
    )

    commands = [
        "echo 2"
    ]

    def check_command(self):
        if self.last_user_input == "echo 1":
            text = (
                "\nBernard: {{Bb:\"Ah, trade secret. *wink*\"}}"
            )
            self.send_text(text)
        elif self.last_user_input == "echo 3":
            text = (
                "\nBernard: {{Bb:\"Er, what? No, I wasn't planning "
                "on doing so. Why would I do that?\"}}"
            )
            self.send_text(text)
        elif self.last_user_input == "echo 4":
            text = (
                "\nBernard: {{Bb:\"Oh ho ho ho, that's none of your business.\"}}"
            )
            self.send_text(text)
        else:
            return StepTemplateNano.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    print_text = [
        "{{yb:\"What's the next big tool you want to create?\"}}"
    ]

    story = [
        "Bernard: {{Bb:\"I want to know how the}} "
        "{{bb:private-section}} {{Bb:is locked "
        "in the}} {{bb:library}}{{Bb:, and then make a "
        "key to unlock it.\"}}",

        "\nEleanor: {{Bb:\"I guess the}} {{bb:librarian}} {{Bb:would have locked the "
        "private section.\"}}",

        "{{Bb:Maybe she can tell us how she did it? We should look for "
        "her.\"}}",

        "\n{{lb:Leave}} the {{bb:shed-shop}}."
    ]

    hints = [
        "{{rb:Use}} {{yb:cd}} {{rb:to leave the shed-shop.}}",
        "{{rb:Use}} {{yb:cd ..}} {{rb:to go}} {{lb:back}} {{rb:to town.}}",
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east"
    eleanors_speech = (
        "Eleanor: {{Bb:\"What do you think is hidden in the private-section?}}"
        "\n{{Bb:Maybe Bernard shouldn't see it...\"}}"
    )
    last_step = True

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)
