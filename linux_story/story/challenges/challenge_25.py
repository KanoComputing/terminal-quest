# challenge_25.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_bernard import TerminalMkdirBernard
from linux_story.story.challenges.challenge_26 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateMkdir(TerminalMkdirBernard):
    challenge_number = 25


class Step1(StepTemplateMkdir):
    story = [
        "Bernard: {{Bb:Hello! Shush, don't say a word.}}",

        "{{Bb:I know why you're here. You want a shed!",

        "I have just the thing for you. I have the}} "
        "{{lb:best-shed-maker-in-the-world.sh}}",

        "\nHe seems pretty enthusiastic about it. {{lb:Examine}} the tool "
        "{{lb:best-shed-maker-in-the-world.sh}}",

        "\n{{gb:Use {{ob:TAB}} to speed up your typing.}}"
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    hints = [
        "{{rb:Use}} {{lb:cat}} {{rb:to examine the}} "
        "{{lb:best-shed-maker-in-the-world.sh}}",

        "{{rb:Use}} {{yb:cat best-shed-maker-in-the-world.sh}} "
        "{{rb:to examine the tool.}}"
    ]

    commands = [
        "cat best-shed-maker-in-the-world.sh"
    ]
    eleanors_speech = (
        "Eleanor: {{Bb:Bernard scares me a bit...}}"
    )

    def check_command(self):
        if self.last_user_input == "cat best-horn-in-the-world.sh":
            self.send_text(
                "\n{{rb:You are reading the wrong file! "
                "You want to read}} {{lb:best-shed-maker-in-the-world.sh}}"
                "{{rb:.}}"
            )
        else:
            return StepTemplateMkdir.check_command(self)

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "The tool has an inscription that reads {{lb:mkdir shed}}.",
        "You recognise the command {{lb:mkdir}}. It's what you used "
        "to help Ruth in the farm.",

        "\nBernard: {{Bb:It's like magic! Just run the command, "
        "and you get a new shed.}}",

        "{{Bb:Try it out! Use it with}} "
        "{{yb:./best-shed-maker-in-the-world.sh}}",

        "\n{{gb:Use {{ob:TAB}} to speed up your typing.}}"
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    hints = [
        "{{rb:Do as Bernard says - use}} "
        "{{yb:./best-shed-maker-in-the-world.sh}} "
        "{{rb:to run his script}}"
    ]
    commands = [
        "./best-shed-maker-in-the-world.sh"
    ]
    eleanors_speech = (
        "Eleanor: {{Bb:Isn't that just the same as running}} "
        "{{yb:mkdir shed}}{{Bb:?}}"
    )

    def check_command(self):
        if self.last_user_input == "./best-horn-in-the-world.sh":
            self.send_text(
                "\n{{rb:You're trying to run the wrong script. "
                "You want to run}} "
                "{{yb:./best-shed-maker-in-the-world.sh}}"
            )
        else:
            return StepTemplateMkdir.check_command(self)

    def next(self):
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        "{{lb:Look around}} to see if it created a shed."
    ]
    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    eleanors_speech = (
        "Eleanor: {{Bb:Ah, look over there!}}"
    )

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "It worked! You can see a new shed in the room.",
        "What happens if you run it again?",
        "{{gb:Press UP twice to replay the command.}}"
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"

    hints = [
        "{{rb:See what happens when you run the script again.}}",

        "{{rb:Run the script again using}} "
        "{{yb:./best-shed-maker-in-the-world.sh}} "
        "{{rb:to see what happens.}}"
    ]
    commands = [
        "./best-shed-maker-in-the-world.sh"
    ]
    eleanors_speech = (
        "Eleanor: {{Bb:I don't think this will work...}}"
    )

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "You get the error {{yb:mkdir: cannot create directory `shed': "
        "File exists}}",
        "\nBernard: {{Bb:Of course it won't work second time - "
        "you already have a shed!",

        "I'm working on the next big thing,}} "
        "{{lb:best-horn-in-the-world.sh}}{{Bb:.}}",

        "{{Bb:It can be used to alert anyone that you're coming. "
        "I'm having some teething problems, "
        "but I'm sure I'll fix them soon.}}",

        "\n{{lb:Examine best-horn-in-the-world.sh}} and see if you "
        "can identify the problem.",

        "{{gb:Remember to use {{ob:TAB}}!}}"
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east/shed-shop"
    commands = [
        "cat best-horn-in-the-world.sh"
    ]

    hints = [
        "{{rb:Use}} {{lb:cat}} {{rb:to examine the tool.}}",
        "{{rb:Use}} {{yb:cat best-horn-in-the-world.sh}} {{rb:to examine the "
        "tool.}}"
    ]

    eleanors_speech = (
        "Eleanor: {{Bb:I think this tool is a bit broken.}}"
    )

    def check_command(self):
        if self.last_user_input == "cat best-shed-maker-in-the-world.sh":
            self.send_text(
                "\n{{rb:You're examining the wrong tool. You want to look "
                "at}} {{yb:best-horn-in-the-world.sh}}"
            )

        else:
            return StepTemplateMkdir.check_command(self)

    def next(self):
        Step6()


class Step6(StepTemplateMkdir):
    story = [
        "The tool reads {{yb:eco \"Honk!\"}}",
        "Maybe it should read {{yb:echo \"Honk!\"}} instead...",
        "How could we make changes to this tool?",
        "\nBernard: {{Bb:Ho ho, you look like you understand the problem.}}",
        "Eleanor: {{Bb:If we need extra help, we can go to the "
        "library, it was just outside.}}",
        "\nBefore we go, have a {{lb:look}} in the {{lb:basement}}."
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
        "{{rb:Use}} {{lb:ls}} {{rb:to look through.}}",
        "{{rb:Use}} {{yb:ls basement/}} {{rb:to look inside.}}"
    ]

    eleanors_speech = (
        "Eleanor: {{Bb:OooOOoh, are there sweets in there?}}"
    )

    def next(self):
        Step7()


class Step7(StepTemplateMkdir):
    story = [
        "Bernard: {{Bb:Oooh naughty, you can't look in there.}}",
        "\nLet's {{lb:leave}} the shed shop and go back to town."
    ]

    start_dir = "~/town/east/shed-shop"
    end_dir = "~/town/east"
    hints = [
        "{{rb:Leave the shed-shop using}} {{yb:cd ..}}"
    ]
    eleanors_speech = (
        "Eleanor: {{Bb:Yay, I like the library. Let's go back to town!}}"
    )

    last_step = True

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)
