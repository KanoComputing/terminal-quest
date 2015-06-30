#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges

from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.terminals.terminal_nano import TerminalNano
from kano_profile.apps import (
    save_app_state_variable, load_app_state_variable,
    increment_app_state_variable
)


def record_user_interaction(instance, base_name):
    '''This is to store when the user interacts with Eleanor.

    instance: the class instance.
    '''

    class_instance = instance.__class__.__name__
    challenge_number = instance.challenge_number
    profile_var_name = "{} {} {}".format(
        base_name, challenge_number, class_instance
    )

    # First, try loading the profile variable name
    # If the value is None, then make it True and increment the total.
    already_done = load_app_state_variable("linux-story", profile_var_name)

    # If cat Eleanor has not been done yet in this class, then increment the
    # total
    if not already_done:
        save_app_state_variable("linux-story", profile_var_name, True)
        total_name = "{}_total".format(base_name)
        increment_app_state_variable("linux-story", total_name, 1)

        # If total reaches a certain amount, then can award XP.


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
