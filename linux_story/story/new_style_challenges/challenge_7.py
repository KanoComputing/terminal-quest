# challenge_7.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.IStep import IStep
from linux_story.story.new_terminals.terminal_cd import TerminalCd
from linux_story.story.tasks.TaskTownHall import TaskTownHall


class StepTemplateCd(IStep):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        _("Have a {{lb:look around}} to see what's going on!")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = [_("{{rb:To look around, use}} {{yb:ls}}")]

    def next(self):
        return 7, 2


class Step2(StepTemplateCd):
    story = [
        _("Wow, there's so many people here. Find the {{bb:Mayor}} and {{lb:listen}} to what he has to say.")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "cat Mayor"
    hints = [_("{{rb:Stuck? Type:}} {{yb:cat Mayor}}")]

    def next(self):
        return 7, 3


class Step3(StepTemplateCd):
    story = [
        _("{{wb:Mayor:}} {{Bb:\"Calm down please! We have our best people looking into the disappearances, and we're hoping to have an explanation soon.\"}}\n"),
        _("Something strange is happening. Better check everyone is ok."),
        _("Type {{yb:cat}} to check on the people.")
    ]
    start_dir = "~/town"
    end_dir = "~/town"

    # Use functions here
    command = ""
    all_commands = {
        "cat grumpy-man": _("{{wb:Man:}} {{Bb:\"Help! I don't know what's happening to me. I heard this bell ring, and now my legs have gone all strange.\"}}"),
        "cat young-girl": _("{{wb:Girl:}} {{Bb:\"Can you help me? I can't find my friend Amy anywhere. If you see her, will you let me know?\"}}"),
        "cat little-boy": _("{{wb:Boy:}} {{Bb:\"Pongo? Pongo? Has anyone seen my dog Pongo? He's never run away before...\"}}")
    }

    last_step = True

    def check_command(self, line):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = _("\n{{gb:You look around.}}")
            self.send_hint(hint)
            return False

        # check through list of commands
        self.hints = [
            _("{{rb:Use}} {{yb:%s}} {{rb:to progress.}}") % self.all_commands.keys()[0]
        ]

        end_dir_validated = self.get_fake_path() == self.end_dir

        # if the validation is included
        if (line in self.all_commands.keys()) and end_dir_validated:
            # Print hint from person
            hint = "\n" + self.all_commands[line]

            self.all_commands.pop(line, None)

            if len(self.all_commands) == 1:
                hint += _("\n{{gb:Well done! Check on 1 more person.}}")
            elif len(self.all_commands) > 0:
                hint += _("\n{{gb:Well done! Check on %d more people.}}") % len(self.all_commands)
            else:
                hint += _("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")

            self.send_hint(hint)

        else:
            self.send_stored_hint()

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        return 8, 1
