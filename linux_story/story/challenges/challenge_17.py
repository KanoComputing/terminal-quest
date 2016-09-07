# challenge_17.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from kano_profile.apps import \
    save_app_state_variable, load_app_state_variable

from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_18 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.helper_functions import wrap_in_box


# This is for the challenges that only need ls
class StepTemplateMv(TerminalMv):
    challenge_number = 17


# This is for that challenges that need echo
class StepTemplateEcho(TerminalEcho):
    challenge_number = 17


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        _("You are in your room, standing in front of the {{bb:.chest}} containing all the commands you've learned so far.\n"),
        _("Maybe something else is hidden in the house?\n"),
        _("{{lb:Look}} in the hallway {{lb:behind you}}. Remember, behind you is {{bb:..}}")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    hints = [
        _("{{rb:Look behind you with}} {{yb:ls ../}}")
    ]
    commands = [
        "ls ..",
        "ls ../"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        _("You see doors to your {{bb:garden}}, {{bb:kitchen}}, {{bb:my-room}} and {{bb:parents-room}}."),
        _("We haven't checked out your parents' room properly yet.\n"),
        _("{{lb:Go into your}} {{bb:parents-room}}.")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/parents-room"

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

    path_hints = {
        "~/my-house/my-room": {
            "blocked": _("\n{{rb:Use}} {{yb:cd ..}} {{rb:to go back.}}")
        },
        "~/my-house": {
            "not_blocked": _("\n{{gb:Now go into your}} {{lb:parents-room}}{{gb:.}}"),
            "blocked": _("\n{{rb:Use}} {{yb:cd parents-room}} {{rb:to go in.}}")
        }
    }

    def check_command(self):
        if self.current_path == self.end_dir:
            return True
        elif "cd" in self.last_user_input and not self.get_command_blocked():
            hint = self.path_hints[self.current_path]["not_blocked"]
        else:
            hint = self.path_hints[self.current_path]["blocked"]

        self.send_text(hint)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


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

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


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
        Step5()


# This class is here so if the user checks the diary,
# they get told off
class CheckDiaryStep(StepTemplateMv):
    def __init__(self, check_diary=0):
        self.check_diary = check_diary
        StepTemplateMv.__init__(self)

    def check_command(self):
        checked_diary = load_app_state_variable(
            "linux-story", "checked_mums_diary"
        )
        # Check to see if the kid reads his/her Mum's journal
        if self.last_user_input == 'cat .safe/mums-diary' and \
                not checked_diary:
            self.send_hint(
                _("\n{{rb:You read your Mum\'s diary!}} {{ob:Your nosiness has been recorded.}}")
            )
            save_app_state_variable("linux-story", "checked_mums_diary", True)
            return False

        return StepTemplateMv.check_command(self)


class Step5(CheckDiaryStep):
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

    def next(self):
        Step6(self.check_diary)


class Step6(CheckDiaryStep):
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
        Step7()


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
    last_step = True

    def next(self):
        NextStep(self.xp)
