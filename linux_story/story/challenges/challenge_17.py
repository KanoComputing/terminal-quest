#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_18 import Step1 as NextChallengeStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


# This is for the challenges that only need ls
class StepTemplateMv(TerminalMv):
    challenge_number = 17


# This is for that challenges that need echo
class StepTemplateEcho(TerminalEcho):
    challenge_number = 17


class Step1(StepTemplateMv):
    story = [
        "You are in your room, standing in front of the .chest "
        "containing all the commands you've learned so far.",
        "Maybe something else is hidden in the house?",
        "Look in the hallway behind you.  Remember, behind you is "
        "{{lb:../}}"
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    hints = [
        "{{rb:You can look with}} {{lb:ls}} {{rb:and the hallway behind you "
        "is}} {{lb:../}}{{rb:. The / is there because this is a folder.}}",
        "{{rb:Look behind you with}} {{yb:ls ../}}"
    ]
    commands = [
        "ls ..",
        "ls ../"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "Have you looked in your parents' room yet?",
        "See if there's something hidden in there."
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"

    # Want to check your parents room
    hints = [
        "{{rb:Your parents' room is in}} {{lb:../parents-room}} "
        "{{rb:relative to where you are now.}}",
        "{{rb:Use}} {{yb:ls -a ../parents-room}} {{rb:to look closely "
        "in your parents' room.}}"
    ]

    commands = [
        "ls -a ../parents-room",
        "ls -a ../parents-room/"
    ]

    # This is for the people who are continuing to play from the
    # beginning.
    # At the start, add the farm directory to the file system
    # Also add the map and journal in your Mum's room
    story_dict = {
        "Cobweb, Trotter, Daisy, Ruth": {
            "path": "~/farm/barn"
        },
        "MKDIR, spanner, hammer, saw, tape-measure": {
            "path": "~/farm/toolshed"
        },
        "farmhouse": {
            "path": "~/farm",
            "directory": True
        },
        # this should be added earlier on, but for people who have updated,
        # we should figure out how to give them the correct file system
        "ECHO, mums-diary, map": {
            "path": "~/my-house/parents-room/.safe"
        }
    }

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "You find a {{lb:.safe}} in your parents' room?",
        "I wonder why they've never told you about this? Go into your "
        "parents' room to make it easier to examine."
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/parents-room"
    hints = [
        "{{rb:Use the command}} {{lb:cd}} {{rb:to go into your}} "
        "{{lb:parents-room}}{{rb:.}}",
        "{{rb:Use the command}} {{yb:cd ../parents-room/}} {{rb:to go "
        "into your parents' room.}}"
    ]
    commands = [
        "cd ../parents-room",
        "cd ../parents-room/",
        "cd ~/my-house/parents-room",
        "cd ~/my-house/parents-room/"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "Maybe there's something useful in here.  Look inside the "
        "{{lb:.safe}}."
    ]

    commands = [
        "ls .safe",
        "ls .safe/",
        "ls -a .safe",
        "ls -a .safe/"
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    hints = [
        "{{rb:Look into the}} {{lb:.safe}} {{rb:using}} {{lb:ls}}",
        "{{rb:Use}} {{yb:ls .safe}} {{rb:to look into the .safe.}}"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "So you found your mum's diary?",
        "You probably shouldn't read it...",
        "What else is here?  Let's examine that {{lb:map}}."
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    hints = [
        "{{rb:Use}} {{lb:cat}} {{rb:to read the}} {{lb:map}}{{rb:.}}",
        "{{rb:Use}} {{yb:cat .safe/map}} {{rb:to read the map.}}"
    ]

    commands = "cat .safe/map"

    def __init__(self):
        self.check_diary = 0
        StepTemplateMv.__init__(self)

    def check_command(self, current_dir):

        # Check to see if the kid reads his/her Mum's journal
        if self.last_user_input == 'cat .safe/mums-diary' and \
                self.check_diary == 0:
            self.send_hint(
                '\n{{rb:You read your Mum\'s diary! How could you??}}'
            )
            self.check_diary += 1
            return False

        return StepTemplateMv.check_command(self, current_dir)

    def next(self):
        Step6()


class Step6(StepTemplateEcho):
    story = [
        "So there's a farm around here?",
        "Apparently it's not far from our house, just off the windy road...",
        "What is this {{lb:ECHO}} note?  Take a look."
    ]

    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    commands = "cat .safe/ECHO"
    hints = [
        "{{rb:Use the}} {{lb:cat}} {{rb:command to read the}} {{lb:ECHO}} "
        "{{rb:note.}}",
        "{{rb:Use}} {{yb:cat .safe/ECHO}} {{rb:to read the note.}}"
    ]

    def next(self):
        Step7()


class Step7(StepTemplateEcho):
    story = [
        "Lets test out this command.  What happens when you "
        "use the command {{yb:echo hello}}?"
    ]
    hints = [
        "{{rb:Use the command}} {{yb:echo Hello}}"
    ]
    commands = [
        "echo hello",
        "echo HELLO",
        "echo Hello"
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
