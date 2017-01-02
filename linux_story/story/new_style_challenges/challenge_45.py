#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.IStep import IStep
from linux_story.PlayerLocation import generate_real_path
from linux_story.common import get_username
from linux_story.helper_functions import has_write_permissions
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.new_terminals.terminal_rm import TerminalRm


class StepTemplateRm(IStep):
    TerminalClass = TerminalRm


class StepPeopleInCage(StepTemplateRm):
    commands_done = {
        "cat bell": False,
        "cat Rabbit": False
    }

    def check_command(self, line):
        if line == "cat Rabbit":
            self.send_hint("Rabbit: {{Bb:...}}\nThe rabbit looks frustrated.")
        elif line == "cat bell":
            self.send_hint("The bell glows menacingly.")
        elif line.startswith("cat cage/"):
            self.send_hint(self.cat_people())
        else:
            return StepTemplateRm.check_command(self, line)

    def cat_people(self):
        people = {
            "Mum": "Mum: {{Bb:" + get_username() + ", I'm so glad to see you're safe!}}",

            "Dad": "Dad: {{Bb:I was kidnapped by a rabbit! Although, I don't know how lucid that rabbit is right now. "
                   "It looks almost possessed}}",

            "grumpy-man": "grumpy-man: {{Bb:My legs are fixed. I hope my wife knows I'm safe.}}",
            "Mayor": "Mayor: {{Bb:When I get out of here, I'm going to bring in a law to hunt all rabbits."
                     "I knew they were out to get us people!}}",
            "little-boy": "little-boy: {{Bb:I miss my mummy!}}",
            "young-girl": "young-girl: {{Bb:I miss my mummy!}}",
            "Edith": "Edith: {{Bb:You, " + get_username() + "! Get us out of here!}}",
            "Edward": "Edward: {{Bb:Edith dear, calm down...}}",
            "dog": "dog: {{Bb:Woof woof!}}",
            "head-librarian": "head-librarian: {{Bb:Who are you?}}",
            "swordmaster": "Swordmaster: {{Bb:" + get_username() + ", don't worry about us, we're safe. The "
                                                                   "Rabbit hasn't figured the sudo password yet.}}"
        }
        for person in people:
            if self._last_user_input == "cat cage/" + person:
                return people[person]

        return ""


class Step1(StepPeopleInCage):
    story = [
        "You are in the rabbithole. {{lb:Look around.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "ls",
        "ls ./",
        "ls ."
    ]

    def next(self):
        return 45, 2


class Step2(StepPeopleInCage):
    story = [
        "You see the rabbit in front of you, a cage and a mysteriously glowing bell.",
        "Swordmaster: {{Bb:Hey! Inside the cage! We're all here!}}",
        "",
        "{{lb:Look inside the cage.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{rb:Use}} {{yb:ls cage}} {{rb:to look inside the cage.}}"
    ]
    commands = [
        "ls cage",
        "ls cage/"
    ]

    def next(self):
        return 45, 3


class Step3(StepPeopleInCage):
    story = [
        "You see all the people who were kidnapped inside the cage.",
        "Swordmaster: {{Bb:Hey, listen, I have something important to say.}}",
        "",
        "{{lb:Listen}} to what the swordmaster has to say."
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{rb:Use}} {{yb:cat cage/swordmaster}} {{rb:to listen to the swordmaster.}}"
    ]
    commands = [
        "cat cage/swordmaster"
    ]

    def next(self):
        return 45, 4


class Step4(StepPeopleInCage):
    story = [
        "Swordmaster: {{Bb:Listen, the Rabbit is possessed.}}",
        "{{Bb:I've seen this rabbit before in the woods, and it was innocent then.}}",
        "{{Bb:I think}} {{lb:the bell}} {{Bb:is to blame here.}}",
        "",
        "{{lb:Examine}} the bell."
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{rb:Use}} {{yb:cat bell}} {{rb:to examine the bell.}}"
    ]
    commands = [
        "cat bell"
    ]

    def next(self):
        return 45, 5


class Step5(StepPeopleInCage):
    story = [
        "The bell glows menacingly.",
        "",
        "Swordmaster: {{Bb:The rabbit hasn't figured out how to use what it stole.}}",
        "{{Bb:Before it does, get us out of this cage. We're locked up in here.}}",
        "",
        "{{lb:You need to unlock the cage.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "Swordmaster: {{Bb:We're all trapped in here because the}} {{lb:write}} {{Bb:permissions are removed.}}",
        "Swordmaster: {{Bb:To re-add the write permissions, use}} {{yb:chmod +w cage}}"
    ]

    def check_command(self, line):
        if has_write_permissions(generate_real_path("~/woods/thicket/rabbithole/cage")):
            return True
        self.send_stored_hint()

    def next(self):
        return 45, 6


class Step6(StepPeopleInCage):
    story = [
        "Swordmaster: {{Bb:Now move us to the}} {{bb:~/town.}}",
        "{{Bb:To move a large group of people, use the}} {{lb:*}} {{Bb:character.}}",
        "{{Bb:Use}} {{yb:mv cage/* ~/town}} {{Bb:to move all of us back to town.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{rb:Use}} {{yb:mv cage/* ~/town}} {{rb:to move all the villagers into the town.}}"
    ]
    commands = [
        "mv cage/* ~/town",
        "mv cage/* ~/town/"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 45, 7


class Step7(StepTemplateRm):
    story = [
        "{{lb:Look in ~/town}} to check that you moved all the people safely."
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "ls ~/town",
        "ls ~/town/"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls ~/town}} {{rb:to check you moved everyone.}}"
    ]

    def next(self):
        return 46, 1
