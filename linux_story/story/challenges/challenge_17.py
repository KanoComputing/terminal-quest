#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story


from linux_story.Step import Step
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_18 import Step1 as NextChallengeStep


# This is for the challenges that only need ls
class StepTemplateMv(Step):
    challenge_number = 17

    def __init__(self, xp=""):
        Step.__init__(self, TerminalMv, xp)


# This is for that challenges that need echo
class StepTemplateEcho(Step):
    challenge_number = 17

    def __init__(self, xp=""):
        Step.__init__(self, TerminalEcho, xp)


class Step1(StepTemplateMv):
    story = [
        "You are in your room, standing in front of the {{yb:.chest}} "
        "containing all the comands you've learned so far",
        "Maybe something else is hidden in the house?",
        "Have you looked in your parent's room yet?"
    ]
    start_dir = "~/my-house/my-room"

    # Keep this unspecified
    end_dir = "~/my-house/my-room"

    # Want to check your parents room
    hints = ["{{rb:Is there anything in your parent's room?}}"]

    # This is for the people who are continuing to play from the
    # beginning.
    # At the start, add the farm directory to the file system
    # Also add the map and journal in your Mum's room
    story_dict = {
        "Cobweb, Trotter, Daisy": {
            "path": "~/farm/barn"
        },
        "Ruth": {
            "path": "~/farm/farmhouse"
        },
        # this should be added earlier on, but for people who have updated,
        # we should figure out how to give them the correct file system
        "ECHO, mums-diary, map": {
            "path": "~/my-house/parents-room/.safe"
        }
    }

    def __init__(self, xp=""):
        self.fork = 0
        StepTemplateMv.__init__(self, xp)

    # Deactivate check_command
    def check_command(self, arg1, arg2):
        return False

    def check_output(self, output):
        # Want output to contain the mums-diary file from your mum
        if not output:
            self.send_hint()
            return False

        if '.safe' in output:
            self.fork = 2
            return True
        elif 'mums-diary' in output:
            self.fork = 3
            return True
        elif 'tv' in output:
            # looking in parents room, but not using ls -a
            self.send_text("\n{{rb:Remember to use}} {{yb:ls -a}} "
                           "{{rb:when looking in your}} {{yb:parents-room}}")
            return False
        else:
            self.send_hint()
            return False

    def next(self):
        if self.fork == 2:
            Step2()
        elif self.fork == 3:
            Step3()


class Step2(StepTemplateMv):
    story = [
        "You find a {{yb:.safe}} in your parent's room?",
        "I wonder why they've never told you about this? Go into your parent's room to make it easier to examine."
    ]
    start_dir = "my-room"
    end_dir = "parents-room"
    hints = [
        "{{rb:Use the command}} {{yb:cd}} {{rb:to go into your}} {{yb:parents-room}}"
    ]

    # Maybe this should be more refined
    def block_command(self, line):
        if "mv" in line:
            return True
        return False

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "Maybe there's something useful in here.  Look inside the {{yb:.safe}}."
    ]

    commands = ["ls", "ls -a"]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    hints = [
        "{{rb:Look into the}} {{yb:.safe}} {{rb:using}} {{yb:ls}}"
    ]

    # This is simply to get the current_dir
    def check_command(self, current_dir, line):
        self.current_dir = current_dir
        StepTemplateMv.check_command(self, current_dir, line)

    def check_output(self, output):
        # Want output to contain the .journal file from your mum

        if not output:
            return False

        if 'mums-diary' in output:
            return True

        self.send_hint()

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "So you found your mum's diary?",
        "You probably shouldn't read it...",
        "What else is here?  Lets have a closer look at that {{yb:map}}"
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    hints = [
        "{{rb:Use}} {{yb:cat}} {{rb:to read the}} {{yb:map}}"
    ]

    command = "cat .safe/map"

    def __init__(self):
        self.check_diary = 0
        StepTemplateMv.__init__(self)

    def check_command(self, line, current_dir):
        line = line.strip()

        # Check to see if the kid reads his/her Mum's journal
        if line == 'cat .safe/mums-diary' and self.check_diary == 0:
            self.send_hint('\n{{rb:You read your Mum\'s diary! How could you?}}')
            self.check_diary += 1
            return False

        return_value = StepTemplateMv.check_command(self, line, current_dir)
        return return_value

    def next(self):
        Step5()


class Step5(StepTemplateEcho):
    story = [
        "So there's a farm around here?",
        "Apparently it's not far from our house, just off the windy road...",
        "What is this {{yb:ECHO}} note?  Take a look."
    ]

    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    commands = "cat .safe/ECHO"
    hints = [
        "{{rb:Use the}} {{yb:cat}} {{rb:command to read the note}}",
        "{{rb:Use}} {{yb:cat .safe/ECHO}} {{rb:to read the note}}"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateEcho):
    story = [
        "Lets test out this command.  What happens when you "
        "use the command {{yb:echo Hello}}?"
    ]
    hint = [
        "{{rb:Use the command}} {{yb:echo Hello}}"
    ]
    commands = "echo Hello"
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"

    def next(self):
        NextChallengeStep(self.xp)
