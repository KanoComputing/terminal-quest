#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.Step import Step
from linux_story.step_helper_functions import unblock_command_list
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_21 import Step1 as NextChallengeStep


class StepTemplateEcho(Step):
    challenge_number = 20

    def __init__(self, xp=''):
        Step.__init__(self, TerminalEcho, xp)


class StepTemplateMkdir(Step):
    challenge_number = 20

    def __init__(self, xp=''):
        Step.__init__(self, TerminalMkdir, xp)


class Step1(StepTemplateEcho):
    story = [
        "Ruth: {{Bb:Oh that's a good idea!  My husband used "
        "to build special shelters to store the crops in. They'd keep everything safe over winter. I think he used a specific tool. "
        "We should take a look in his toolshed to see if we can find it "
        "\n{{gb:Use}} {{yb:cd}} {{gb:to go into the toolshed}}"
    ]

    command = [
        "cd ../toolshed",
        "cd ../toolshed/"
    ]

    start_dir = "barn"
    end_dir = "toolshed"

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        # Move Ruth into the toolshed
        self.story_dict = {
            "Ruth": {
                "path": "~/farm/toolshed"
            }
        }
        self.modify_file_tree()
        Step2()


class Step2(StepTemplateEcho):
    story = [
        "Ruth follows you into the toolshed.  It's a very large "
        "space with tools lining the walls.",
        "Ruth: {{Bb:Lets have a look around for anything that "
        "could be useful}}"
    ]
    start_dir = "toolshed"
    end_dir = "toolshed"

    def check_output(self, output):
        if "MKDIR" in output:
            return True
        return False

    def next(self):
        Step3()


# We could have a lot of items in the shed.  We should encourage
# the user to cat the,
class Step3(StepTemplateEcho):
    story = [
        "Ruth: {{Bb:Ah, look! A note.",
        "I think this is what he used to use?",
        "What does it say?}}"
    ]
    hints = [
        "Ruth: {{Bb:\"...you are able to read, yes? You can use}} {{yb:cat}} "
        "{{Bb:to read things\"}}",
        "Ruth: {{Bb:\"Just use}} {{yb:cat MKDIR}} {{Bb:\"}}"
    ]
    start_dir = "toolshed"
    end_dir = "toolshed"
    command = "cat MKDIR"

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:This says you can make something using something "
        "called}} {{yb:mkdir}}{{Bb:?}}",
        "\n{{gb:Try making an igloo using }} {{yb:mkdir}}"
    ]
    hints = [
        "{{rb:Create an igloo structure by using}} {{yb:mkdir igloo}}"
    ]
    start_dir = "toolshed"
    end_dir = "toolshed"
    command = "mkdir igloo"

    def check_command(self, line, current_dir):
        line = line.strip()
        if line == "cat MKDIR":
            self.send_hint("\n{{gb:Well done for checking the page again!}}")
            return False

        return StepTemplateMkdir.check_command(self, line, current_dir)

    def next(self):
        Step5()
        # NextChallengeStep(self.xp)


class Step5(StepTemplateMkdir):
    story = [
        "Now have a look around and see what's changed"
    ]
    start_dir = "toolshed"
    end_dir = "toolshed"
    command = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./"
    ]

    def next(self):
        NextChallengeStep(self.xp)
