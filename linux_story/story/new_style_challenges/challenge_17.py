# challenge_17.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from kano_profile.apps import save_app_state_variable, load_app_state_variable

from linux_story.IStep import IStep
from linux_story.common import get_story_file
from linux_story.story.new_terminals.terminal_mv import TerminalMv
from linux_story.story.new_terminals.terminal_echo import TerminalEcho
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.helper_functions import wrap_in_box


# This is for the challenges that only need ls
class StepTemplateMv(IStep):
    TerminalClass = TerminalMv


# This is for that challenges that need echo
class StepTemplateEcho(IStep):
    TerminalClass = TerminalEcho


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        _("You are in your room, standing in front of the {{bb:.chest}} containing all the commands you've learned so far.\n"),
        _("Maybe something else is hidden in the house?\n"),
        _("{{lb:Look}} in the hallway {{lb:behind you}}. Remember, behind you is {{bb:..}}")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    file_list = [
        {"path": "~/farm/barn/Cobweb"},
        {"path": "~/farm/barn/Daisy"},
        {"path": "~/farm/barn/Ruth"},
        {"path": "~/farm/barn/Trotter"},
        {"path": "~/farm/toolshed/MKDIR"},
        {"path": "~/farm/toolshed/spanner"},
        {"path": "~/farm/toolshed/hammer"},
        {"path": "~/farm/toolshed/saw"},
        {"path": "~/farm/toolshed/tape-measure"},
        {
            "path": "~/farm/farmhouse/bed",
            "contents": get_story_file("bed_farmhouse")
        },
        {"path": "~/farm/toolshed/MKDIR"},
        {"path": "~/my-house/parents-room/.safe/ECHO"},
        {"path": "~/my-house/parents-room/.safe/mums-diary"},
        {"path": "~/my-house/parents-room/.safe/map"}
    ]
    hints = [
        _("{{rb:Look behind you with}} {{yb:ls ../}}")
    ]
    commands = [
        "ls ..",
        "ls ../"
    ]

    def next(self):
        return 17, 2


class Step2(StepTemplateMv):
    story = [
        _("You see doors to your {{bb:garden}}, {{bb:kitchen}}, {{bb:my-room}} and {{bb:parents-room}}."),
        _("We haven't checked out your parents' room properly yet.\n"),
        _("{{lb:Go into your}} {{bb:parents-room}}.")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/parents-room"

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 17, 3


class Step3(StepTemplateMv):
    story = [
        _("Look around {{lb:closely}}.")
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"

    hints = [
        _("{{rb:Use the command}} {{yb:ls -a}} {{rb:to look around closely.}}")
    ]
    commands = [
        "ls -a",
        "ls -a .",
        "ls -a ./"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 17, 4


class Step4(StepTemplateMv):
    story = [
        _("There's a {{bb:.safe}}!\n"),
        _("Maybe there's something useful in here. {{lb:Look inside}} the {{bb:.safe}}.")
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
        _("{{rb:Look in the}} {{bb:.safe}} {{rb:using}} {{lb:ls}}{{rb:.}}"),
        _("{{rb:Use}} {{yb:ls .safe}} {{rb:to look into the .safe.}}")
    ]

    def next(self):
        return 17, 5


class Step5(StepTemplateMv):
    story = [
        _("So you found your {{bb:Mum's diary}}?"),
        _("You probably shouldn't read it...\n"),
        _("What else is here? Let's {{lb:examine}} that {{bb:map}}.")
    ]
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    hints = [
        _("{{rb:Use}} {{yb:cat}} {{rb:to read the}} {{bb:map}}{{rb:.}}"),
        _("{{rb:Use}} {{yb:cat .safe/map}} {{rb:to read the map.}}")
    ]

    commands = "cat .safe/map"

    def check_command(self, line):
        checked_diary = load_app_state_variable("linux-story", "checked_mums_diary")
        if line == 'cat .safe/mums-diary' and not checked_diary:
            self.send_hint(_("\n{{rb:You read your Mum\'s diary!}} {{ob:Your nosiness has been recorded.}}"))
            save_app_state_variable("linux-story", "checked_mums_diary", True)
            return False

        return StepTemplateMv.check_command(self, line)

    def next(self):
        return 17, 6


class Step6(StepTemplateMv):
    story = [
        _("So there's a farm around here?"),
        _("Apparently it's not far from our house, just off the windy road...\n"),
        _("What is this {{bb:ECHO}} note? {{lb:Examine}} the {{bb:ECHO}} note.")
    ]

    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"
    commands = "cat .safe/ECHO"
    hints = [
        _("{{rb:Use the}} {{yb:cat}} {{rb:command to read the}} {{bb:ECHO}} {{rb:note.}}"),
        _("{{rb:Use}} {{yb:cat .safe/ECHO}} {{rb:to read the note.}}")
    ]

    def next(self):
        return 17, 7


class Step7(StepTemplateEcho):
    story = [
        _("So the note says {{Bb:\"echo hello - will make you say hello\"}}"),
        _("Let's test this out. \n"),
    ]
    story += wrap_in_box([
        _("{{gb:New Spell}}: {{yb:echo}} followed by words"),
        _("lets you {{lb:speak}}"),
    ])

    hints = [
        _("{{rb:Use the command}} {{yb:echo hello}}")
    ]
    commands = [
        "echo hello",
        "echo HELLO",
        "echo Hello"
    ]
    highlighted_commands = ['echo']
    start_dir = "~/my-house/parents-room"
    end_dir = "~/my-house/parents-room"

    def next(self):
        return 18, 1
