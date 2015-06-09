#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.step_helper_functions import (
    unblock_commands_with_cd_hint, unblock_commands_with_mkdir_hint,
    unblock_commands
)
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_22 import Step1 as NextChallengeStep


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 21


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:Nice! You've build an igloo! You learned the new skill, "
        "mkdir!}}",
        "\nRuth: {{Bb:That's amazing!  Please help me build a shelter!",
        "Can we build it in the}} {{lb:barn}}{{Bb:, as then it'll be easier "
        "to move the animals inside.}}",
        "\n{{yb:Go back into the barn.}}"
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/barn"
    commands = [
        "cd ../barn/",
        "cd ../barn",
        "cd ~/farm/barn",
        "cd ~/farm/barn/"
    ]
    hints = [
        "{{rb:Try using}} {{yb: cd ../barn/}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:Anyone can find the igloo, "
        "can we make something that people can't find. Do you have "
        "any ideas how we can make something hidden?}}\n",
        "{{yb:1: If we call it}} {{lb:hidden-shelter}}"
        "{{yb:, that will make it hidden.}}",
        "{{yb:2: Putting a . at the front makes things hidden.}}",
        "{{yb:3: It's impossible to make a hidden shelter.}}\n",
        "Use echo to tell Ruth how to make things hidden."
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]
    hints = [
        "Ruth: {{Bb:You're really going to have to speak up, "
        "I can't understand anything you're saying.}}",
        "{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} "
        "{{yb:echo 3}} {{rb:to reply to Ruth.}}"
    ]

    def __init__(self):
        self.next_class = Step4
        StepTemplateMkdir.__init__(self)

    def check_command(self, current_dir):
        if self.last_user_input == "echo 1":
            self.next_class = Step3a
            return True
        elif self.last_user_input == "echo 2":
            self.next_class = Step3b
            return True
        elif self.last_user_input == "echo 3":
            hint = (
                "\nRuth: {{Bb:...Really? Are you sure about that?}}"
            )
            self.send_text(hint)
        else:
            self.send_hint()

    def next(self):
        self.next_class()


# Fork a - try making a hidden shelter
class Step3a(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:So creating one called}} {{lb:hidden-shelter}} "
        "{{Bb:should make it hidden?  Ok, let's try that.}}\n",
        "Try making a shelter called {{lb:hidden-shelter}}."
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "mkdir hidden-shelter",
    ]
    hints = [
        "{{rb:You need to make a shelter called}} {{yb:hidden-shelter}}"
        "{{rb:.}}",
        "{{rb:Use the command}} {{yb:mkdir hidden-shelter}} "
        "{{rb:to make the shelter.}}"
    ]

    def check_command(self, current_dir):
        if self.last_user_input == "mkdir .hidden-shelter":
            hint = (
                "\nRuth: {{Bb:You said the shelter should be called}} "
                "{{lb:hidden-shelter}}{{Bb:, not}} {{lb:.hidden-shelter}}"
                "{{Bb:.}}"
            )
            self.send_text(hint)
        else:
            return StepTemplateMkdir.check_command(self, current_dir)

    def block_command(self):
        return unblock_commands_with_mkdir_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step4a()


class Step4a(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:You made}} {{lb:hidden-shelter!}}",
        "{{Bb:...The problem is, I can see it too.  I don't think it worked.",
        "How else could you make something hidden?}}\n",
        "{{yb:1: If you put a . in front of the name, it makes it hidden.}}",
        "{{yb:2: You're mistaken. You can't see the hidden-shelter, it's "
        "hidden.}}\n",
        "Use echo to talk to Ruth.",
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "echo 1"
    ]
    hints = [
        "Ruth: {{Bb:You NEED to speak more clearly. I can't understand you.}}",
        "{{rb:Use}} {{yb:echo 1}} {{rb:or}} {{yb:echo 2}} {{rb:to reply.}}"
    ]

    def check_command(self, current_dir):
        if self.last_user_input == "echo 1":
            return True

        elif self.last_user_input == "echo 2":
            hint = (
                "\nRuth: {{Bb:....",
                "Be careful kid, I'm not stupid. That shelter is not hidden.\n"
                "How do I make one that is?}}"
            )
            self.send_text(hint)

        else:
            self.send_hint()

    def next(self):
        Step3b()


###########################################
# Second fork

class Step3b(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:So if we called the shelter}} {{lb:.shelter}}"
        "{{Bb:, it would be hidden?  Let's try it!}}",
        "Make a shelter called {{lb:.shelter}}"
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    hints = [
        "{{rb:Make}} {{lb:.shelter}} {{rb:using}} {{yb:mkdir .shelter}}"
        "{{rb: - remember the dot!}}"
    ]
    commands = [
        "mkdir .shelter"
    ]

    def block_command(self):
        return unblock_commands_with_mkdir_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Check it is properly hidden. Use {{yb:ls}} to "
        "see if it is visible.",
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    commands = [
        "ls"
    ]

    hints = [
        "{{rb:Use}} {{yb:ls}}{{rb, not ls -a, to check your shelter "
        "is hidden.}}"
    ]

    def check_command(self, current_dir):
        if self.last_user_input == "ls -a":
            self.send_hint(
                "{{rb:Use}} {{yb:ls}} {{rb:instead of}} {{yb:ls -a}} "
                "{{yb:to check it's hidden.}}"
            )
        else:
            return StepTemplateMkdir.check_command(self, current_dir)

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Now look around with {{yb:ls -a}} to check it actually exists!"
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls -a}} {{rb:to look around}}"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:Did you make something? That's amazing!",
        "...unfortunately I can't see it...please can you put me "
        "and the animals inside?}}\n",
        "Move everyone into the {{lb:.shelter}} "
        "one by one using {{yb:mv <name> .shelter}}\n"
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    all_commands = [
        "mv Trotter .shelter/",
        "mv Trotter .shelter",
        "mv Daisy .shelter/",
        "mv Daisy .shelter",
        "mv Cobweb .shelter/",
        "mv Cobweb .shelter",
        "mv Ruth .shelter/",
        "mv Ruth .shelter"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.all_commands)

    def check_command(self, current_dir):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if self.last_user_input == 'ls' or self.last_user_input == "ls -a":
            hint = "\n{{gb:Well done for looking around.}}"
            self.send_text(hint)
            return False

        # check through list of commands
        end_dir_validated = False
        self.hints = [
            "{{rb:Use}} {{yb:" + self.all_commands[0] + "}} "
            "{{rb:to progress}}"
        ]

        end_dir_validated = current_dir == self.end_dir

        # if the validation is included
        if self.last_user_input in self.all_commands and \
                end_dir_validated:

            # Remove both elements, with a slash and without a slash
            if self.last_user_input[-1] == "/":
                self.all_commands.remove(self.last_user_input)
                self.all_commands.remove(self.last_user_input[:-1])
            else:
                self.all_commands.remove(self.last_user_input)
                self.all_commands.remove(self.last_user_input + "/")

            if len(self.all_commands) == 1:
                hint = (
                    "\n{{gb:Well done! Move one more in the}}"
                    " {{yb:.shelter}}"
                )
            elif len(self.all_commands) > 0:
                hint = "\n{{gb:Well done! Move " + \
                    str(len(self.all_commands) / 2) + \
                    " more.}}"
            else:
                hint = "\n{{gb:Press Enter to continue}}"

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        Step7()


class Step7(StepTemplateMkdir):
    story = [
        "Head into the {{yb:.shelter}} along with Ruth and the "
        "animals."
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn/.shelter"
    commands = [
        "cd .shelter",
        "cd .shelter/"
    ]
    hints = [
        "{{rb:Type}} {{yb:cd .shelter/}} {{rb:to go into the}} "
        "{{lb:.shelter}}{{rb:.}}"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step8()


class Step8(StepTemplateMkdir):
    story = [
        "Have a look around with {{yb:ls}} to check you moved everyone."
    ]
    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"
    commands = ["ls"]
    hints = ["Look around using {{yb:ls}}"]
    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
