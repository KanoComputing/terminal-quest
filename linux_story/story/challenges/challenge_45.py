#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.Animation import Animation
from linux_story.common import get_username
from linux_story.helper_functions import has_write_permissions
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.terminals.terminal_rm import TerminalRm
from linux_story.story.challenges.challenge_46 import Step1 as NextStep


class StepTemplateRm(TerminalRm):
    challenge_number = 45


class Step1(StepTemplateRm):
    story = [
        "You are in the rabbithole. Look around."
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "ls",
        "ls ./",
        "ls ."
    ]

    def next(self):
        Step2()


class Step2(StepTemplateRm):
    story = [
        "You see the rabbit in front of you, a cage and a mysteriously glowing bell.",
        "Swordmaster: {{Bb:Hey! Inside the cage! We're all here!}}",
        "",
        "{{lb:Look inside the cage.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "Use {{yb:ls cage}} to look inside the cage."
    ]  # don't show hints for this section
    commands = [
        "ls cage",
        "ls cage/"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateRm):
    story = [
        "You see all the people who were kidnapped inside the cage, including the swordmaster.",
        "Swordmaster: {{Bb:Hey, listen, I have something important to say.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "Use {{yb:cat swordmaster}} to listen to the swordmaster."
    ]
    commands = [
        "cat cage/swordmaster"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateRm):
    story = [
        "Swordmaster: {{Bb:Listen, the Rabbit is possessed.}}",
        "{{Bb:I've seen this rabbit before in the woods, and it's never behaved like this before.}}",
        "{{Bb:I think}} {{lb:the bell}} {{Bb:is to blame here.}}",
        "",
        "{{lb:Examine}} {{Bb:the bell.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "Use {{yb:cat bell}} to examine the bell."
    ]
    # could you examine the bell first, and through the rabbit, it either pleads with you, or tries to corrupt you?
    # It could give you a fake password prompt in order to try and get your private details.
    # Maybe it could ask for your facebook account password as a way of trying to get more information from you?
    commands = [
        "cat bell"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateRm):
    story = [
        "The bell glows menacingly.",
        "",
        "Swordmaster: {{Bb:The rabbit hasn't figured out}} {{lb:how to use what it stole.}}",
        "{{Bb:Before it does, save all the villagers.}}",
        "{{Bb:We're all trapped in this cage.}}",
        "{{lb:First}}, {{lb:uncage us}}{{Bb:.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{Bb:Think back to the cave in the woods.}}",
        "{{Bb:The villagers are trapped because the write permissions are removed.}}",
        "{{Bb:To re-add the write permissions, use}} {{yb:chmod +w cage}}"
    ]

    def check_command(self):
        # check the write (and execute) permissions on the cage
        if has_write_permissions(self.generate_real_path("~/woods/thicket/rabbithole")):
            return True
        self.send_hint()

    def next(self):
        Step6()


class Step6(StepTemplateRm):
    story = [
        "Swordmaster: {{Bb:Now move us to the}} {{bb:~/town.}}",
        "{{Bb:To move a large group of people, use the}} {{lb:*}} {Bb:character.}}",
        "{{Bb:Use}} {{yb:mv cage/* ~/town}} {{Bb:to move all people back to town.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "Use {{yb:mv cage/* ~/town}} to move all the villagers into the town."
    ]
    commands = [
        "mv cage/* ~/town",
        "mv cage/* ~/town/"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        NextStep()



###############################################################################
class Step100(StepTemplateRm):
    story = [
        "You see the rabbit in front of you, a cage and a mysteriously glowing bell. Investigate."
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [""]  # don't show hints for this section
    commands_done = {
        "cat bell": False,
        "cat Rabbit": False
    }

    def check_command(self):
        story = ""
        if self.last_user_input == "cat Rabbit":
            story = "Rabbit: {{Bb:...}}\nThe rabbit looks frustrated."
        if self.last_user_input == "cat bell":
            story = "The bell glows menacingly."
        if self.last_user_input.startswith("cat cage/"):
            story = self.cat_people()
        self.send_hint(story)

        if self.last_user_input in self.commands_done:
            self.commands_done[self.last_user_input] = True

        for command in self.commands_done:
            if not self.commands_done[command]:
                return False

        return True

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
            if self.last_user_input == "cat cage/" + person:
                return people[person]

        return ""

    def next(self):
        Step101()


class Step101(StepTemplateRm):
    story = [
        "Swordmaster: {{Bb:What are you waiting for?",
        "You need to}} {{yb:remove the source of the problem.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "rm bell"
    ]

    def block_command(self):
        if self.last_user_input == "rm Rabbit":
            self.send_hint("Swordmaster: {{Bb:I don't think that is the source of the problem...}}")
            return True
        return StepTemplateRm.block_command(self)

    def next(self):
        # TODO play animation of the bell being destroyed?
        # Then the rabbit blinking, and the text of the rabbit saying ""
        # Animation("firework-animation").play_finite(cycles=1)
        # self.send_hint("Done!")
        Animation()
