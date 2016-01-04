#!/usr/bin/env python

# commands.py
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Classes with Linux command functionality


import os


class CommandMissingDoFunction(Exception):
    pass


class CommandMissingAutocompleteFunction(Exception):
    pass


class Command(object):
    '''
    This is a template for the other linux commands.
    '''

    def __init__(self, user=None):
        # This is an instance of the User class
        # it is initialised elsewhere so the user data is consistent between
        # commands
        self._user = user

    @property
    def filesystem(self):
        return self._user.filesystem

    @property
    def position(self):
        return self._user.position

    def set_position(self, position):
        return self._user.set_position(position)

    def do(self):
        '''
        This is where the main functionality for the command should be put
        '''
        pass

    def autocomplete(self, line):
        '''
        If user presses tab after this command, this funciton should return
        a list of suggested completions.
        '''
        return []

    def _parse_input(self, line):
        '''
        If the user input contains the command word, this strips that command
        word off. Useful for autocomplete functions.

        :param line: user input, e.g. cd dir/
        :type line: string
        :returns: line with command word stripped off, e.g. dir1/
        :rtype: string
        '''
        words = line.split(" ")
        parsed_input = " ".join(words[1:]).strip()
        return parsed_input


class Echo(Command):

    def do(self, line):
        return line


class Pwd(Command):

    def do(self, line):
        return self.position


class Ls(Command):

    def __init__(self, user):
        self._rv = {
            "files": [],
            "message": ""
        }
        return super(Ls, self).__init__(user)

    def do(self, line):
        '''
        This should be called if the user does `ls line` in the terminal.
        Returns information about any error messages, and details about the
        list of iles that the user should see.
        It is done this way so the view can then colour the output
        appropriately.

        :param line: line that the user enters after using the ls
        :type line: string
        :returns: information about any error messages and the FileObjects
                  and Dictionary objects located
        :rtype: a dictionary of the form {"files": list of FileObjects,
                                           "message": string}
        '''
        if not line:
            return self._no_args()
        return self._no_flags(line)

    def _no_such_file_message(self, line):
        self._rv["message"] = (
            "ls: {}: No such file or directory".format(line)
        )
        return self._rv

    def _show_ls_at_position(self, position):
        self._rv["files"] = self.filesystem.get_all_at_path(position)
        return self._rv

    def _no_args(self):
        '''
        Behaviour of ls when it is alone
        '''
        return self._show_ls_at_position(self.position)

    def _no_flags(self, line):
        '''
        Behaviour of ls without any of the flags like -l -a
        '''
        path = os.path.join(self.position, line)
        (exists, f) = self.filesystem.path_exists(path)
        if not exists:
            return self._no_such_file_message(line)

        if not f.has_read_permission(self._user.name):
            self._rv["message"] = "ls: {}: Permission denied".format(line)
            return self._rv

        if f.type == "file":
            self._rv["message"] = line
            return self._rv
        elif f.type == "directory":
            self._rv["files"] = f.children
            return self._rv

    def autocomplete(self, line):
        line = self._parse_input(line)
        return autocomplete(line, self.position, self.filesystem, "all")


class Cd(Command):

    def do(self, line):
        if not line:
            return self._no_args()

        return self._no_flags(line)

    def _no_such_file_message(self, name):
        return "cd: no such file or directory: {}".format(name)

    def _cd_into_file(self, name):
        return "bash: cd: {}: Not a directory".format(name)

    def _no_args(self):
        self.set_position("~")

    def _no_flags(self, line):
        path = os.path.normpath(os.path.join(self.position, line))
        (exists, f) = self.filesystem.path_exists(path)
        if not exists:
            return self._no_such_file_message(line)
        elif not f.type == "directory":
            return self._cd_into_file(line)
        elif not f.has_execute_permission(self._user.name):
            return "cd: permission denied: {}".format(line)
        else:
            self._user.set_position(path)

    def autocomplete(self, line):
        # needed for Cmd module, which handles the tab_once/tab_many
        # condition
        line = self._parse_input(line)
        return autocomplete(line, self.position, self.filesystem, "dirs")


class Cat(Command):

    def do(self, line):
        if not line:
            self._no_arguments()
            return

        return self._no_flags(line)

    def _no_arguments(self):
        '''
        cat without arguments just echos out what the user last
        typed. Change this behaviour and pass message to the user.
        '''
        return ("Use the format \"cat filepath\" for a filepath of "
                "your choice.")

    def _no_such_file_message(self, name):
        return "cat: {}: no such file or directory".format(name)

    def _no_flags(self, line):
        path = os.path.join(self.position, line)

        (exists, f) = self.filesystem.path_exists(path)
        if not exists:
            return self._no_such_file_message(line)
        elif not f.has_read_permission(self._user.name):
            return "cat: {}: Permission denied".format(line)
        else:
            return f.content

    def autocomplete(self, line):
        line = self._parse_input(line)
        return autocomplete(line, self.position, self.filesystem, "all")


def autocomplete(line, position, filesystem, config):
    '''
    :params line: the line typed on the command line so far
    :type line: str
    :params position: path
    :type position: str
    :params filesystem: set of object you want returned - FileObjects,
                        Directory objects or both
    :params config: "all", "files", "dirs"
    '''
    completions = []

    if not line:
        # Add slash after all directories
        directories = filesystem.get_dirnames_at_path(position)
        directories = [d + "/" for d in directories]
        files = []

        if config == "all":
            files = filesystem.get_filenames_at_path(position)

        completions = directories + files
    else:
        final_text = line.split("/")[-1]
        complete_path = "/".join(line.split("/")[:-1])
        path = os.path.join(
            position, complete_path
        )
        exists, f = filesystem.path_exists(path)
        if exists and f.type == "directory":
            for child in f.children:
                if child.name.startswith(final_text):
                    if child.type == "directory":
                        completions.append(child.name + "/")
                    elif config == "all":
                        completions.append(child.name)

    return sorted(completions)
