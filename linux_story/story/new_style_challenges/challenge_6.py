# challenge_6.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
from linux_story.story.new_terminals.terminal_cd import TerminalCd


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        _("Let {{bb:Mum}} know about {{bb:Dad}}. Type {{yb:cat Mum}}")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    commands = "cat Mum"
    hints = [_("{{rb:To talk to your Mum, type}} {{yb:cat Mum}} {{rb:and press}} {{ob:Enter}}{{rb:.}}")]

    def next(self):
        return 6, 2


class Step2(StepTemplateCd):
    story = [
        _("{{wb:Mum:}} {{Bb:\"You couldn't find him? That's strange, he never leaves home without telling me first.\""),
        _("\"Maybe he went to that town meeting with the Mayor, the one they were talking about on the news. "
          "Why don't you go and check? I'll stay here in case he comes back.\"}}\n"),
        _("Let's head to {{bb:town}}. To leave the house, use {{yb:cd}} by itself.")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~"
    commands = "cd"
    hints = [_("{{rb:Type}} {{yb:cd}} {{rb:to start the journey.}}")]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 6, 3


class Step3(StepTemplateCd):
    story = [
        _("You're out of the house and on the long windy road called Tilde, or {{bb:~}}"),
        _("{{lb:Look around}} again to see where to go next.")
    ]
    start_dir = "~"
    end_dir = "~"
    commands = "ls"
    hints = [_("{{rb:Stuck? Type}} {{yb:ls}} {{rb:to look around.}}")]

    def next(self):
        return 6, 4


class Step4(StepTemplateCd):
    story = [
        _("You can see a {{bb:town}} in the distance! Let's {{lb:go}} there using {{lb:cd}}.")
    ]
    start_dir = "~"
    end_dir = "~/town"
    commands = ["cd town", "cd town/"]
    hints = [_("{{rb:Type}} {{yb:cd town}} {{rb:to walk into town.}}")]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 7, 1
