# challenge_25.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.challenges.CompanionMisc import StepTemplateMkdir
from linux_story.step_helper_functions import unblock_cd_commands


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        _("Bernard: {{Bb:\"Hello! Shush, don't say a word.\"}}"),

        _("{{Bb:\"I know why you're here. You want a shed!\""),

        _("\"I have just the thing for you. I have the}} " +\
        "{{bb:best-shed-maker-in-the-world.sh}}{{Bb:\"}}"),

        _("\nHe seems pretty enthusiastic about it. {{lb:Examine}} the tool " +\
        "{{bb:best-shed-maker-in-the-world.sh}}"),

        _("\n{{gb:Use}} {{ob:TAB}} {{gb:to speed up your typing.}}")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    hints = [
        _("{{rb:Use}} {{yb:cat}} {{rb:to examine the}} " +\
        "{{bb:best-shed-maker-in-the-world.sh}}"),

        _("{{rb:Use}} {{yb:cat best-shed-maker-in-the-world.sh}} " +\
        "{{rb:to examine the tool.}}")
    ]

    commands = [
        "cat best-shed-maker-in-the-world.sh",
        "cat ./best-shed-maker-in-the-world.sh"
    ]
    companion_speech = _("Eleanor: {{Bb:Bernard scares me a bit...}}")

    def check_command(self, line):
        if line == "cat best-horn-in-the-world.sh" or \
                        line == "cat ./best-horn-in-the-world.sh":

            self.send_hint(
                _("\n{{rb:You are reading the wrong file! " +\
                "You want to read}} {{bb:best-shed-maker-in-the-world.sh}}" +\
                "{{rb:.}}")
            )
        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 25, 2


class Step2(StepTemplateMkdir):
    story = [
        _("The tool has an inscription that reads \"mkdir shed\"."),
        _("You recognise the command {{yb:mkdir}}. It's what you used " +\
        "to help {{bb:Ruth}} in the farm."),

        _("\nBernard: {{Bb:It's like magic! Just run the command, " +\
        "and you get a new shed.}}"),

        _("{{Bb:Try it out! Use it with}} " +\
        "{{yb:./best-shed-maker-in-the-world.sh}}"),

        _("\n{{gb:Use}} {{ob:TAB}} {{gb:to speed up your typing.}}")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    hints = [
        _("{{rb:Do as Bernard says - use}} " +\
        "{{yb:./best-shed-maker-in-the-world.sh}} " +\
        "{{rb:to run his script}}")
    ]
    commands = [
        "./best-shed-maker-in-the-world.sh"
    ]
    companion_speech = \
        _("Eleanor: {{Bb:Isn't that just the same as running}} " +\
        "{{yb:mkdir shed}}{{Bb:?}}")

    def check_command(self, line):
        if line == "./best-horn-in-the-world.sh":
            self.send_hint(
                _("\n{{rb:You're trying to run the wrong script. " +\
                "You want to run}} " +\
                "{{yb:./best-shed-maker-in-the-world.sh}}")
            )
        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 25, 3


class Step3(StepTemplateMkdir):
    story = [
        _("{{lb:Look around}} to see if it created a {{bb:shed}}.")
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]
    companion_speech = _("Eleanor: {{Bb:Ah, look over there!}}")

    def next(self):
        return 25, 4


class Step4(StepTemplateMkdir):
    story = [
        _("It worked! You can see a new {{bb:shed}} in the room.\n"),
        _("What happens if you run it again?\n"),
        _("{{gb:Press}} {{ob:UP}} {{gb:twice to replay the command.}}")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    hints = [
        _("{{rb:See what happens when you run the script again.}}"),

        _("{{rb:Run the script again using}} " +\
        "{{yb:./best-shed-maker-in-the-world.sh}} " +\
        "{{rb:to see what happens.}}")
    ]
    commands = [
        "./best-shed-maker-in-the-world.sh"
    ]
    companion_speech = _("Eleanor: {{Bb:I don't think this will work...}}")

    def next(self):
        return 25, 5


class Step5(StepTemplateMkdir):
    story = [
        _("You get the error {{yb:mkdir: cannot create directory `shed': " +\
        "File exists}}"),
        _("\nBernard: {{Bb:\"Of course it won't work a second time - " +\
        "you already have a shed!\""),

        _("\"I'm working on the next big thing,}} " +\
        "{{bb:best-horn-in-the-world.sh}}{{Bb:.\"}}"),

        _("{{Bb:\"It can be used to alert anyone that you're coming. " +\
        "I'm having some teething problems, " +\
        "but I'm sure I'll fix them soon.\"}}"),

        _("\n{{lb:Examine}} {{bb:best-horn-in-the-world.sh}} {{lb:and see if you " +\
        "can identify the problem.}}\n"),

        _("{{gb:Remember to use}} {{ob:TAB}}{{gb:!}}")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    commands = [
        "cat best-horn-in-the-world.sh",
        "cat ./best-horn-in-the-world.sh"
    ]

    hints = [
        _("{{rb:Use}} {{yb:cat}} {{rb:to examine the tool.}}"),
        _("{{rb:Use}} {{yb:cat best-horn-in-the-world.sh}} {{rb:to examine the " +\
        "tool.}}")
    ]

    companion_speech = (
        _("Eleanor: {{Bb:I think this tool is a bit broken.}}")
    )

    def check_command(self, line):
        if line == "cat best-shed-maker-in-the-world.sh" or \
           line == "cat ./best-shed-maker-in-the-world.sh":

            self.send_hint(
                _("\n{{rb:You're examining the wrong tool. You want to look " +\
                "at}} {{yb:best-horn-in-the-world.sh}}")
            )

        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 25, 6


class Step6(StepTemplateMkdir):
    story = [
        _("The tool reads {{yb:eco \"Honk!\"}}"),
        _("Maybe it should read {{yb:echo \"Honk!\"}} instead..."),
        _("How could we make changes to this tool?"),
        _("\nBernard: {{Bb:\"Ho ho, you look like you understand the problem.\"}}"),
        _("Eleanor: {{Bb:\"If we need extra help, we can go to the " +\
        "library, it was just outside.\"}}"),
        _("\nBefore we go, have a {{lb:look}} in the {{bb:basement}}.")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    commands = [
        "ls basement",
        "ls basement/",
        "ls -a basement",
        "ls -a basement/",
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look through.}}"),
        _("{{rb:Use}} {{yb:ls basement/}} {{rb:to look inside.}}")
    ]

    companion_speech = (
        _("Eleanor: {{Bb:OooOOoh, are there sweets in there?}}")
    )

    def check_command(self, line):
        # Using self._last_user_input because the line param is empty from being blocked.
        if self._last_user_input in self.commands:
            return True
        return StepTemplateMkdir.check_command(self, self._last_user_input)

    def next(self):
        return 25, 7


class Step7(StepTemplateMkdir):
    story = [
        _("Bernard: {{Bb:\"Oooh naughty, you can't look in there.\"}}"),
        _("\nLet's {{lb:leave}} the shed shop and go back to {{bb:east}} of town.")
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east"
    hints = [
        _("{{rb:Leave the shed-shop using}} {{yb:cd ..}}")
    ]
    companion_speech = (
        _("Eleanor: {{Bb:\"Yay, I like the library. Let's go back to town!\"}}")
    )

    def block_command(self, line):
        if line.startswith("cd"):
            return unblock_cd_commands(line)
        else:
            return StepTemplateMkdir.block_command(self, line)

    def next(self):
        return 26, 1
