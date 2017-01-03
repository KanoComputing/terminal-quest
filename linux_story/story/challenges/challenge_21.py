# challenge_21.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.step_helper_functions import unblock_cd_commands, unblock_commands_with_mkdir_hint, unblock_commands
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir


class StepTemplateMkdir(StepTemplate):
    TerminalClass = TerminalMkdir


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        _("{{gb:Nice! You've built an igloo! You learned the new skill, " +\
        "mkdir!}}"),
        _("\nRuth: {{Bb:\"That's amazing! Please help me build a shelter!"),
        _("Can we build it in the}} {{bb:barn}}{{Bb:, as then it'll be easier " +\
        "to move the animals inside.\"}}"),
        _("\n{{lb:Go}} back into the {{bb:barn}}.")
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/barn"
    deleted_items = [
        "~/farm/toolshed/Ruth"
    ]
    file_list = [
        {"path": "~/farm/barn/Ruth"}
    ]

    path_hints = {
        "~/farm/toolshed": {
            "blocked": _("\n{{rb:Use}} {{yb:cd ..}} {{rb:to go back.}}")
        },
        "~/farm": {
            "not_blocked": _("\n{{gb:You walk outside. Now go into the}} {{bb:barn}}{{gb:.}}"),
            "blocked": _("\n{{rb:Use}} {{yb:cd barn}} {{rb:to go in the barn.}}")
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
        return 21, 2


class Step2(StepTemplateMkdir):
    story = [
        _("Ruth: {{Bb:\"Anyone would be able to find the igloo " +\
        "you just made."),
        _("Is it possible to make something hidden?\"}}\n"),
        _("{{yb:1: \"If we call it}} {{bb:hidden-shelter}}" +\
        "{{yb:, that will make it hidden.\"}}"),
        _("{{yb:2: \"Putting a . at the front makes things hidden.\"}}"),
        _("{{yb:3: \"It's impossible to make a hidden shelter.\"}}\n"),
        _("Use {{yb:echo}} to tell {{bb:Ruth}} how to make things hidden.")
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]
    hints = [
        _("Ruth: {{Bb:\"You're really going to have to speak up, " +\
        "I can't understand anything you're saying.\"}}"),
        _("{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} " +\
        "{{yb:echo 3}} {{rb:to reply to Ruth.}}")
    ]

    def _run_at_start(self):
        self.__next_step = 4

    def check_command(self, line):
        if line == "echo 1":
            self.__next_step = 3
            return True
        elif line == "echo 2":
            self.__next_step = 6
            return True
        elif line == "echo 3":
            hint = (
                _("\nRuth: {{Bb:\"...Really? Are you sure about that?\"}}")
            )
            self.send_hint(hint)
        else:
            self.send_stored_hint()

    def next(self):
        return 21, self.__next_step


# First fork - try making a hidden shelter
class Step3(StepTemplateMkdir):
    print_text = [
        _("{{yb:\"If we call it}} {{bb:hidden-shelter}}" +\
        "{{yb:, that will make it hidden.\"}}")
    ]
    story = [
        _("Ruth: {{Bb:\"So creating one called}} {{bb:hidden-shelter}} " +\
        "{{Bb:should make it hidden? Ok, let's try that.\"}}\n"),
        _("Try {{lb:building}} a shelter called {{bb:hidden-shelter}}.")
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "mkdir hidden-shelter",
    ]
    hints = [
        _("{{rb:You need to make a shelter called}} {{yb:hidden-shelter}}" +\
        "{{rb:.}}"),
        _("{{rb:Use the command}} {{yb:mkdir hidden-shelter}} " +\
        "{{rb:to make the shelter.}}")
    ]

    def check_command(self, line):
        if line == "mkdir .hidden-shelter":
            hint = (
                _("\nRuth: {{Bb:\"You said the shelter should be called}} " +\
                "{{bb:hidden-shelter}}{{Bb:, not}} {{lb:.hidden-shelter}}" +\
                "{{Bb:.\"}}" +\
                "\n{{yb:Press UP to replay the old command, and edit it.}}")
            )
            self.send_hint(hint)
        else:
            return StepTemplateMkdir.check_command(self, line)

    def block_command(self, line):
        return unblock_commands_with_mkdir_hint(line, self.commands)

    def next(self):
        return 21, 4


class Step4(StepTemplateMkdir):
    story = [
        _("{{lb:Look around}} to see if it is hidden correctly.")
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "ls"
    ]
    hints = [
        _("{{rb:Look around with}} {{yb:ls}}{{rb:.}}")
    ]
    ls_a_hint = True

    def check_command(self, line):
        if line == "ls -a" and self.ls_a_hint:
            hint = (
                _("\n{{gb:Close!}} {{ob:But you need to check if the " +\
                "shelter is hidden, so don't look " +\
                "around you}} {{yb:too closely}}{{rb:.}}")
            )
            self.send_hint(hint)
            self.ls_a_hint = False
        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 21, 5


class Step5(StepTemplateMkdir):
    story = [
        _("Ruth: {{Bb:\"You made}} {{bb:hidden-shelter}}{{Bb:!\"}}"),
        _("{{Bb:\"...The problem is, I can see it too. I don't think it worked."),
        _("How else could you make something hidden?\"}}"),
        _("\n{{yb:1: \"If you put a . in front of the name, it makes it hidden.\"}}"),
        _("{{yb:2: \"You're mistaken. You can't see the hidden-shelter, it's " +\
        "hidden.\"}}\n"),
        _("Use {{yb:echo}} to talk to {{bb:Ruth}}."),
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "echo 1"
    ]
    hints = [
        _("Ruth: {{Bb:You NEED to speak more clearly. I can't understand you.}}"),
        _("{{rb:Use}} {{yb:echo 1}} {{rb:or}} {{yb:echo 2}} {{rb:to reply.}}")
    ]

    def check_command(self, line):
        if line == "echo 1":
            return True

        elif line == "echo 2":
            hint = (
                _("\nRuth: {{Bb:....") +\
                _("Be careful kid, I'm not stupid. That shelter is not hidden.\n") +\
                _("How do I make one that is?}}")
            )
            self.send_hint(hint)

        else:
            self.send_stored_hint()

    def next(self):
        return 21, 6


###########################################
# Second fork

class Step6(StepTemplateMkdir):
    print_text = [
        _("{{yb:\"If you put a . in front of the name, it makes it hidden.\"}}")
    ]
    story = [
        _("Ruth: {{Bb:\"So if we called the shelter}} {{bb:.shelter}}" +\
        "{{Bb:, it would be hidden? Let's try it!\"}}\n"),
        _("{{lb:Build}} a shelter called {{bb:.shelter}}")
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    hints = [
        _("{{rb:Make}} {{bb:.shelter}} {{rb:using}} {{yb:mkdir .shelter}}" +\
        "{{rb: - remember the dot!}}")
    ]
    commands = [
        "mkdir .shelter"
    ]

    def block_command(self, line):
        return unblock_commands_with_mkdir_hint(line, self.commands)

    def next(self):
        return 21, 7


class Step7(StepTemplateMkdir):
    story = [
        _("Check it is properly hidden. Use {{yb:ls}} to see if it is visible.")
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    commands = [
        "ls"
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls}}{{rb:, not ls -a, to check your shelter " +\
        "is hidden.}}")
    ]

    def next(self):
        return 21, 8


class Step8(StepTemplateMkdir):
    story = [
        _("{{gb:Good, we can't see it in the barn.}}\n"),
        _("Now look around with {{yb:ls -a}} to check it actually exists!")
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = [
        "ls -a"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls -a}} {{rb:to look around.}}")
    ]

    def next(self):
        return 21, 9


class Step9(StepTemplateMkdir):
    story = [
        _("{{gb:It worked! You've succesfully created something hidden.}}"),
        _("\nRuth: {{Bb:\"Did you make something? That's amazing!\""),
        _("\"...unfortunately I can't see it...please can you put me " +\
        "and the animals inside?\"}}\n"),
        _("{{lb:Move}} everyone into the {{bb:.shelter}} " +\
        "one by one.\n")
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

    def block_command(self, line):
        return unblock_commands(line, self.all_commands)

    def check_command(self, line):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if line == 'ls' or line == "ls -a":
            hint = _("\n{{gb:You look around.}}")
            self.send_hint(hint)
            return False

        # check through list of commands
        self.hints = [
            _("{{rb:Use}} {{yb:%s}} {{rb:to progress}}") % (self.all_commands[0],)
        ]

        end_dir_validated = self.get_fake_path() == self.end_dir

        # if the validation is included
        if line in self.all_commands and end_dir_validated:

            # Remove both elements, with a slash and without a slash
            if line[-1] == "/":
                self.all_commands.remove(line)
                self.all_commands.remove(line[:-1])
            else:
                self.all_commands.remove(line)
                self.all_commands.remove(line + "/")

            if len(self.all_commands) == 1:
                hint = (
                    _("\n{{gb:Well done! Move one more in the}} {{yb:.shelter}}")
                )
            elif len(self.all_commands) > 0:
                hint = _("\n{{gb:Well done! Move %s more.}}")\
                    % str(len(self.all_commands) / 2)
            else:
                hint = _("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue}}")

            self.send_hint(hint)

        else:
            self.send_hint("\n" + self.hints[0])

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        return 21, 10


class Step10(StepTemplateMkdir):
    story = [
        _("{{lb:Go}} into the {{bb:.shelter}} along with {{bb:Ruth}} and the " + \
        "animals.")
    ]
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn/.shelter"
    hints = [
        _("{{rb:Type}} {{yb:cd .shelter}} {{rb:to go into the}} " + \
        "{{bb:.shelter}}{{rb:.}}")
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 21, 11


class Step11(StepTemplateMkdir):
    story = [
        _("Have a {{lb:look around}} to check you moved everyone.")
    ]
    start_dir = "~/farm/barn/.shelter"
    end_dir = "~/farm/barn/.shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Look around using}} {{yb:ls}}{{rb:.}}")
    ]

    def next(self):
        return 22, 1
