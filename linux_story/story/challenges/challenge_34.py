#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.step_helper_functions import unblock_commands
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.challenges.challenge_35 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 34


class StepTemplateChmod(TerminalChmod):
    challenge_number = 34


class Step1(StepTemplateNano):
    story = [
        "There are three rooms.",
        "Lets look at each of the rooms in turn.",
        "First, {{lb:look inside the dark-room}}."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls dark-room",
        "ls dark-room/"
    ]
    hints = [
        "Use {{lb:ls dark-room/}} to look inside the dark-room."
    ]

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "The room is pitch black, and it is impossible to see anything inside.",
        "Next, look inside the {{bb:locked-room}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls locked-room",
        "ls locked-room/"
    ]
    hints = [
        "Use {{lb:ls locked-room/}} to look inside the locked-room."
    ]

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Peering through a grimy window, you can just make out the items inside.",
        "{{lb:Examine the items inside}}."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    dirs_to_attempt = "~/woods/cave/locked-room"
    commands = [
        "cat locked-room/sign",
        "cat locked-room/firework"
    ]
    hints = [
        "Examine the sign with {{lb:cat locked-room/sign}}."
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "You are unable to make out the items in the room.",
        "Finally, look inside the {{bb:cage}}."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls cage",
        "ls cage/"
    ]
    hints = [
        "Look inside the cage with {{yb:ls cage}}"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    story = [
        "There is a bird in the cage. {{lb:Examine}} the bird.",
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat cage/bird"
    ]
    hints = [
        "Examine the bird with {{yb:cat cage/bird}}"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateChmod):
    story = [
        "Bird: {{Bb:...Me...trapped..}}",
        "{{Bb:Please help....get me out.}}",
        "",
        "Try and help the bird by {{lb:moving}} the bird outside the cage."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "mv cage/bird .",
        "mv cage/bird ./"
    ]
    hints = [
        "Move the bird outside the cage with {{yb:mv cage/bird ./}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step7()



class Step7(StepTemplateChmod):
    story = [
        "That didn't work. You can't seem to move the bird outside the cage.",
        "Bird: {{Bb:...didn't work....}}",
        "{{Bb:...look in}} {{lb:dark-room}} {{Bb:to find help..}}",
        "{{Bb:..use}} {{yb:chmod +r dark-room}} {{Bb:to switch lights on.}}",
        "{{Bb:...get me out...and I'll help you.}}"
    ]

    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "chmod +r dark-room",
        "chmod +r dark-room/"
    ]
    hints = [
        "{{lb:Follow the bird's instructions and use}} {{yb:chmod +r dark-room}} {{lb:to turn the lights on.}}"
    ]

    def next(self):
        NextStep()


# class Step4(StepTemplateNano):
#     story = [
#         "The sign suggests we should {{lb:move the lighter}} from the {{bb:cage-room}} to the {{bb:locked-room}}",
#         "Look around to find the lighter."
#     ]
#     start_dir = "~/woods/cave"
#     end_dir = "~/woods/cave"
#     commands = [
#         "ls cage-room",
#         "ls cage-room/",
#         "mv cage-room/lighter locked-room",
#         "mv cage-room/lighter locked-room/"
#     ]
#
#     def next(self):
#         if self.commands.index(self.last_user_input) <= 1:
#             Step3()
#         else:
#             Step4()
#
#
# class Step2(StepTemplateNano):
#     story = [
#         "There are three rooms, and a sign.",
#         "{{lb:Look in all the rooms}} and see if you find anything interesting."
#     ]
#     start_dir = "~/woods/cave"
#     end_dir = "~/woods/cave"
#     task = TaskCaveCheckRooms()
#
#     def check_command(self):
#         if self.task.passed(self.last_user_input):
#             return True
#
#         self.send_hint(self.task.get_hint_text(self.last_user_input))
#
#     def next(self):
#         Step2()
#
#
# class Step2(StepTemplateNano):
#     story = [
#         "The only room you seem to be able to look inside is the cage-room.",
#         "{{lb:Examine all the items inside.}}"
#     ]
#     start_dir = "~/woods/cave"
#     end_dir = "~/woods/cave"
#     commands = [
#         "cat cage-room/sign"
#     ]
#     hints = [
#         "{{lb:Read}} at the sign in the cage-room."
#     ]
#
#     def check_command(self):
#         if self.last_user_input == "cat cage-room/bird":
#             self.send_hint("The bird looks dejected.\nWhat does the sign say?")
#             return
#
#         return StepTemplateNano.check_command(self)
#
#     def next(self):
#         Step3()
#
#
# class Step3(StepTemplateChmod):
#     story = wrap_in_box([
#         _("{{gb:New Spell:}} Type {{yb:chmod +r}} and press"),
#         _("{{ob:Enter}} to {{lb:light up a dark room}}."),
#     ])
#     story += [
#         "The sign suggests we should use this in the dark-room.",
#         "Try it."
#     ]
#
#     commands = [
#         "ls dark-room",
#         "ls dark-room/"
#     ]
#
#     start_dir = "~/woods/cave"
#     end_dir = "~/woods/cave"
#
#     hints = [
#         "Use {{yb:ls dark-room}} to look inside"
#     ]
#
#     def next(self):
#         Step4()
#
#
# class Step4(StepTemplateChmod):
#     story = [
#         "You cannot see anything, because the lights are off",
#         "To turn on the lights, {{lb:use the command you learnt.}}"
#     ]
#     start_dir = "~/woods/cave"
#     end_dir = "~/woods/cave"
#     commands = [
#         "chmod +r dark-room",
#         "chmod +r dark-room/"
#     ]
#     hints = [
#         "Use {{yb:chmod +r dark-room}} to light up the dark-room."
#     ]
#
#     def next(self):
#         NextStep()