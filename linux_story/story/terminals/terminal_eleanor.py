#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges

from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.helper_functions import record_user_interaction


class TerminalMkdirEleanor(TerminalMkdir):
    eleanors_speech = ""

    def check_command(self):
        if self.last_user_input == "cat Eleanor":
            self.eleanor_speaks()
            record_user_interaction(self, "cat_eleanor")

        else:
            return TerminalMkdir.check_command(self)

    def eleanor_speaks(self):
        '''Use this to get Eleanor to "speak"
        '''
        if self.eleanors_speech:
            self.send_text("\n" + self.eleanors_speech)


class TerminalNanoEleanor(TerminalNano):
    eleanors_speech = ""

    def check_command(self):
        if self.last_user_input == "cat Eleanor":
            self.eleanor_speaks()
            record_user_interaction(self, "cat_eleanor")

        else:
            return TerminalNano.check_command(self)

    def eleanor_speaks(self):
        '''Use this to get Eleanor to "speak"
        '''
        if self.eleanors_speech:
            self.send_text("\n" + self.eleanors_speech)
