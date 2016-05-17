#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

# from linux_story.Step import Step
from linux_story.story.terminals.terminal_cat import TerminalCat
from linux_story.story.challenges.challenge_4 import Step1 as NextChallengeStep


class StepTemplateCat(TerminalCat):
    challenge_number = 3


class Step1(StepTemplateCat):
    story = [
        _("Love it! Put it on quickly."),
        _("There's loads more interesting stuff in your room."),
        _("Let's {{lb:look}} in your {{lb:shelves}} using {{lb:ls}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = ["ls shelves", "ls shelves/"]
    hints = _("{{rb:Type}} {{yb:ls shelves/}} {{rb:to look at your books.}}")

    def next(self):
        Step2()


class Step2(StepTemplateCat):
    story = [
        _("Did you know you can use the TAB key to speed up your typing?"),
        _("Try it by checking out that comic book. {{lb:Examine}} it with "
        "{{yb:cat shelves/comic-book}}"),
        _("Press the TAB key before you've finished typing!\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat shelves/comic-book"
    hints = _("{{rb:Type}} {{yb:cat shelves/comic-book}} {{rb:to read the comic.}}")

    def next(self):
        Step3()


class Step3(StepTemplateCat):
    story = [
        _("Why is it covered in pawprints?"),
        _("Hang on, can you see that? There's a {{lb:note}} amongst your books."),
        _("{{lb:Read}} the note using {{lb:cat}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat shelves/note"
    hints = _("{{rb:Type}} {{yb:cat shelves/note}} {{rb:to read the note.}}")

    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
