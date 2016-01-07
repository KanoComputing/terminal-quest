#!/usr/bin/env python

# terminal.py
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Contains classes that model a terminal.


from cmd import Cmd
import os
from new_linux_story.models.filesystem import FileSystem
from new_linux_story.models.commands import Ls, Cd, Cat, Pwd, Echo
from new_linux_story.models.User import User
from linux_story.helper_functions import colour_string_with_preset


class TerminalBase(object):
    def __init__(self, config, position, cmd):
        self._user = User(FileSystem(config), position)
        self._cmd = cmd
        self._ls = Ls(self._user)
        self._cd = Cd(self._user)
        self._cat = Cat(self._user)
        self._pwd = Pwd(self._user)
        self._echo = Echo()

    @property
    def filesystem(self):
        return self._user.filesystem

    @property
    def position(self):
        return self._user.position

    def create_prompt(self, location):

        # if prompt ends with / strip it off
        if location[-1] == '/':
            location = location[:-1]

        # Put together the terminal prompt.
        username = os.environ['LOGNAME']
        yellow_part = username + "@kano "
        yellow_part = colour_string_with_preset(yellow_part, "yellow", True)

        blue_part = location + ' $ '
        blue_part = colour_string_with_preset(blue_part, "blue", True)
        return yellow_part + blue_part

    def do_ls(self, line):
        output = self._ls.do(line)
        message = output["message"]
        files = output["files"]

        if message:
            print message
        else:
            coloured = []
            for f in files:
                if f.type == "directory":
                    coloured.append(
                        colour_string_with_preset(
                            f.name, "blue", True
                        )
                    )
                elif f.type == "file":
                    coloured.append(f.name)
            print " ".join(coloured)

    def complete_ls(self, line):
        return self._ls.autocomplete(line)

    def do_cd(self, line):
        output = self._cd.do(line)
        if output:
            print output
        self._cmd.prompt = self.create_prompt(self.position)

    def complete_cd(self, line):
        return self._cd.autocomplete(line)

    def do_cat(self, line):
        print self._cat.do(line)

    def complete_cat(self, line):
        return self._cat.autocomplete(line)


class CmdBase(Cmd):
    def __init__(self, config, position):
        Cmd.__init__(self)
        self._terminal = TerminalBase(config, position, self)
        self.prompt = self._terminal.create_prompt(position)


class Terminal1(CmdBase):

    def do_ls(self, line):
        return self._terminal.ls(line)

    def complete_ls(self, text, line, begidx, endidx):
        return self._terminal.complete_ls(line)


class Terminal2(CmdBase):

    def do_cd(self, line):
        return self._terminal.do_cd(line)

    def complete_cd(self, text, line, begidx, endidx):
        return self._terminal.complete_cd(line)


class Terminal3(CmdBase):

    def do_ls(self, line):
        return self._terminal.do_ls(line)

    def complete_ls(self, text, line, begidx, endidx):
        return self._terminal.complete_ls(line)

    def do_cd(self, line):
        return self._terminal.do_cd(line)

    def complete_cd(self, text, line, begidx, endidx):
        return self._terminal.complete_cd(line)

    def do_cat(self, line):
        return self._terminal.do_cat(line)

    def complete_cat(self, text, line, begidx, endidx):
        return self._terminal.complete_cat(line)
