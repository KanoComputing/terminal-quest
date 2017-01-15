#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges
import getpass
from linux_story.story.terminals.terminal_rm import TerminalRm


class TerminalSudo(TerminalRm):
    terminal_commands = [
        "ls", "cat", "cd", "mv", "echo", "mkdir", "nano", "chmod", "rm", "sudo"
    ]

    def do_sudo(self, line):
        command = line.split(" ")[0]
        following_line = " ".join(line.split(" ")[1:])

        if command in self.terminal_commands:
            success_cb = getattr(self, 'do_{}'.format(command))
        else:
            success_cb = lambda *cb_args: printf("sudo: " + line + ": command not found")

        self.__sudo(self._location.get_real_path(), line, success_cb, 0, following_line)

    def __sudo(self, real_path, line, success_cb, counter=0, *cb_args):

        if counter == 0:
            self._client.send_hint("\n{{gb:Type a password. You won't be able to see what you type.}}")
        elif counter == 3:
            self.passed = False
            print "sudo: 3 incorrect password attempts"
            return

        user = getpass.getuser()
        password = getpass.getpass('[sudo] password for {}:'.format(user))

        # For now hard code the password?
        if password != "kano":
            print "Sorry, try again."
            counter += 1
            if password == "" and counter < 3:
                self._client.send_hint("\n{{rb:You didn't type anything! You need to type a password!}}")
            return self.__sudo(real_path, line, success_cb, counter, *cb_args)

        self.passed = True
        if success_cb:
            success_cb(*cb_args)


def printf(text):
    print text
