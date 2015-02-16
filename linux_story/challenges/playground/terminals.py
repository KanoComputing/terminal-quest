#!/usr/bin/env python

# Terminals.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The main terminal class.


import os
import sys


terminal_path = os.path.abspath(__file__)
dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from ..commands_fake import cd
from ..commands_real import ls, sudo, grep, shell_command, launch_application
from terminal import Terminal

# If this is not imported, the escape characters used for the colour prompts
# show up as special characters. We don't use any functions from this module,
# simply importing this module fixes the bug
import readline


class Complete_Terminal(Terminal):

    def __init__(self, start_dir, end_dir, validation, hints=[""]):
        Terminal.__init__(self, start_dir, end_dir, validation, hints=[""])

    #######################################################
    # Custom commands

    def do_ls(self, line):
        ls(self.current_dir, self.filetree, line)

    def complete_ls(self, text, line, begidx, endidx):
        text = text.split(" ")[-1]
        return self.autocomplete_desc(text, line, "both")

    def do_cd(self, line):
        dir = cd(self.current_dir, self.filetree, line)
        if dir:
            self.current_dir = dir
            self.set_prompt()

    def complete_cd(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "dirs")

     # modified like ls to show colours
    def do_grep(self, line):
        grep(self.current_dir, self.filetree, line)

    #######################################################
    # Standard commands called in the shell

    # Commands autocompleted on pressing TAB

    def do_mv(self, line):
        shell_command(self.current_dir, self.filetree, line, "mv")
        self.update_tree()

    def complete_mv(self, text, line, begidx, endidx):
        completions = self.autocomplete_desc(text, line, "both")
        return completions

    def do_rm(self, line):
        shell_command(self.current_dir, self.filetree, line, "rm")
        self.update_tree()

    def complete_rm(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")

    def do_cp(self, line):
        shell_command(self.current_dir, self.filetree, line, "cp")
        self.update_tree()

    def complete_cp(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")

    def do_cat(self, line):
        shell_command(self.current_dir, self.filetree, line, "cat")

    def complete_cat(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")

    def do_wc(self, line):
        shell_command(self.current_dir, self.filetree, line, "wc")

    def complete_wc(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")

    def do_more(self, line):
        launch_application(self.current_dir, self.filetree, line, "more")

    def complete_more(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")

    def do_chmod(self, line):
        shell_command(self.current_dir, self.filetree, line, "chmod")

    def complete_chmod(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")

    # Commands not autocompleted on pressing TAB

    def do_mkdir(self, line):
        shell_command(self.current_dir, self.filetree, line, "mkdir")
        self.update_tree()

    def do_touch(self, line):
        shell_command(self.current_dir, self.filetree, line, "touch")
        self.update_tree()

    def do_passwd(self, line):
        shell_command(self.current_dir, self.filetree, line, "passwd")
        self.update_tree()

    def do_xargs(self, line):
        shell_command(self.current_dir, self.filetree, line, "xargs")

    def do_sudo(self, line):
        sudo(self.current_dir, self.filetree, line)

    def do_clear(self, line):
        shell_command(self.current_dir, self.filetree, line, "clear")

    def do_find(self, line):
        shell_command(self.current_dir, self.filetree, line, "find")

    def do_pwd(self, line):
        shell_command(self.current_dir, self.filetree, line, "pwd")

    def do_alias(self, line):
        shell_command(self.current_dir, self.filetree, line, "alias")

    def do_unalias(self, line):
        shell_command(self.current_dir, self.filetree, line, "unalias")

    #######################################################
    # Commands that do not use piping when using subprocess

    def do_nano(self, line):
        launch_application(self.current_dir, self.filetree, line, "nano")

    def complete_nano(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")

    def do_less(self, line):
        launch_application(self.current_dir, self.filetree, line, "less")

    def complete_less(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")

    # Tis is listed with the other launched applications because
    # the piping only works if no piping is used
    def do_echo(self, line):
        launch_application(self.current_dir, self.filetree, line, "echo")

    def do_man(self, line):
        launch_application(self.current_dir, self.filetree, line, "man")
