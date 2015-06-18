#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_eleanor import (
    TerminalMkdirEleanor, TerminalNanoEleanor
)
from linux_story.story.challenges.challenge_28 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateMkdir(TerminalMkdirEleanor):
    challenge_number = 27


class StepTemplateNano(TerminalNanoEleanor):
    challenge_number = 27


class Step1(StepTemplateMkdir):
    story = [
        "You are back in the Bernard's place.",
        "{{lb:Listen to what Bernard has to say.}}"
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    hints = [
        "{{rb:Use}} {{yb:cat Bernard}} {{rb:to interact with Bernard.}}"
    ]

    commands = [
        "cat Bernard"
    ]

    deleted_items = ["~/town/east-part/library/Eleanor"]
    story_dict = {
        "Eleanor": {
            "path": "~/town/east-part/shed-shop"
        }
    }
    eleanors_speech = (
        "Eleanor: {{Bb:Achoo! This place is really dusty...*sniff*}}"
    )

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Bernard: {{Bb:Hellooooo. You came back to fix my script!}}",

        "Let's see whether we can fix it.",

        "Let's try and use {{yb:nano best-horn-in-the-world.sh}} to "
        "edit it."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    commands = [
        "nano best-horn-in-the-world.sh"
    ]

    hints = [
        "{{rb:Use}} {{yb:nano best-horn-in-the-world}} "
        "{{rb:to edit the tool.}}"
    ]

    eleanors_speech = (
        "Eleanor: {{Bb:They taught us how to write at school. "
        "I don't think Bernard is very clever.}}"
    )

    goal_nano_end_content = "echo \"Honk!\""
    goal_nano_filepath = "~/town/east-part/shed-shop/best-horn-in-the-world.sh"
    goal_nano_save_name = "best-horn-in-the-world.sh"

    # Overwrite the default behaviour for most of the steps - nano needs
    # slightly different behaviour.
    def check_command(self, current_dir):
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

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    commands = [
        "./best-horn-in-the-world.sh"
    ]

    eleanors_speech = (
        "Eleanor: {{Bb:Will it be loud?}}"
    )

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    # Allow the user to ask all the questions within the same Step?
    story = [
        "{{gb:Congratulations, the script now prints \"Honk!\"}}",

        "\nBernard: {{Bb:The tool is working! Wonderful! "
        "Thank you so much!}}",

        "\nIt occurs to you that you haven't asked Bernard much about "
        "himself.",

        "What would you like to ask him?",

        "\n{{yb:1 \"How did you create your tools?\"}}",

        "{{yb:2: \"What's the next big tool you want to create?\"}}",

        "{{yb:3: \"Are you going into hiding now?\"}}",

        "{{yb:4: \"What's in the secret room?\"}}",

        "\nUse {{lb:echo}} to ask him a question."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    eleanors_speech = (
        "Eleanor: {{Bb:I have a question - does he have candy in his "
        "secret-room?}}"
    )

    commands = [
        "echo 2"
    ]

    def check_command(self, current_dir):
        if self.last_user_input == "echo 1":
            text = (
                "\nBernard: {{Bb:Ah, trade secret. *wink*}}"
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
                "\nBernard: {{Bb:Oh ho ho ho, that's none of your business.}}"
            )
            self.send_text(text)
        else:
            return StepTemplateNano.check_command(self, current_dir)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    print_text = [
        "{{yb:\"What's the next big tool you want to create?\"}}"
    ]

    story = [
        "Bernard: {{Bb:I want to know how the}} "
        "{{lb:private-section}} {{Bb:is locked "
        "in the}} {{lb:library}}{{Bb:, and then make}} "
        "{{lb:best-key-in-the-world.sh}}",

        "\nEleanor: {{Bb:I guess the librarian would have locked it.}}",

        "{{Bb:Maybe she can give us information about where she found "
        "that?",

        "She might have gone into hiding somewhere. We should look "
        "for her.}}",

        "\n{{lb:Leave}} the shed-shop."
    ]

    commands = [
        "cd ..",
        "cd ../"
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part"
    eleanors_speech = (
        "Eleanor: {{Bb:What do you think is hidden in the protected-section?}}"
        "\n{{Bb:Maybe Bernard shouldn't see it...}}"
    )
    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextStep(self.xp)
