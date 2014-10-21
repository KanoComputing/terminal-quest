"""
* Copyright (C) 2014 Kano Computing Ltd
* License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
*
* Author: Caroline Clark <caroline@kano.me>
* The main terminal class.
"""

from cmd import Cmd
import os
import sys
import json

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from commands_fake import cd
from commands_real import ls, sudo, grep, shell_command, launch_application
from Node import generate_file_tree
from helper_functions import copy_file_tree, get_completion_dir
from kano.colours import colourizeInput256, colourize256

NUMBER_OF_CHALLENGES = 8


class Terminal(Cmd):

    def __init__(self, start_dir, end_dir, validation, hint=""):
        Cmd.__init__(self)
        self.update_tree()
        self.current_dir = start_dir
        self.current_path = self.filetree[start_dir]
        self.end_dir = end_dir
        self.validation = validation
        self.hint = hint
        self.set_prompt()
        self.cmdloop()

    def set_prompt(self):
        self.prompt = self.filetree.generate_prompt(self.current_dir)

    # default behaviour - exit the application
    def do_EOF(self, line=None):
        return True

    def validate(self, line):
        command = True
        end_dir = True
        if self.validation:
            command = self.validation == line
        if self.end_dir:
            end_dir = self.current_dir == self.end_dir

        # if user does not pass challenge, show hint
        if not (command and end_dir):
            print colourize256(self.hint, 147, 16, True)

        return command and end_dir

    # do nothing if the user enters an empty line
    def emptyline(self):
        pass

    # only done after commands that change the file structure
    def update_tree(self):
        self.filetree = generate_file_tree()

    # This is the cmd valid command
    def postcmd(self, stop, line):
        return self.validate(line)

    def complete_list(self):
        return list(self.filetree.show_direct_descendents(self.current_dir))

    def do_shell(self, line):
        #"Run a shell command"
        output = os.popen(line).read()
        self.last_output = output

    #######################################################
    # Custom commands

    def do_ls(self, line):
        ls(self.current_dir, self.filetree, line)

    def complete_ls(self, text, line, begidx, endidx):
        text = text.split(" ")[-1]
        completions = self.autocomplete_dir(text, line, begidx, endidx)
        return completions

    def do_cd(self, line):
        dir = cd(self.current_dir, self.filetree, line)
        if dir:
            self.current_dir = dir
            self.set_prompt()

    def complete_cd(self, text, line, begidx, endidx):
        completions = self.autocomplete_dir(text, line, begidx, endidx)
        return completions

     # modified like ls to show colours
    def do_grep(self, line):
        grep(self.current_dir, self.filetree, line)

    #######################################################
    # Standard commands called in the shell

    def do_chmod(self, line):
        line = self.join_command_to_line("chmod", line)
        shell_command(self.current_dir, self.filetree, line)

    def do_touch(self, line):
        line = self.join_command_to_line("touch", line)
        shell_command(self.current_dir, self.filetree, line)
        self.update_tree()

    def do_mkdir(self, line):
        line = self.join_command_to_line("mkdir", line)
        shell_command(self.current_dir, self.filetree, line)
        self.update_tree()

    def complete_mkdir(self, text, line, begidx, endidx):
        completions = self.autocomplete(text, line, begidx, endidx)
        return completions

    def do_mv(self, line):
        line = self.join_command_to_line("mv", line)
        shell_command(self.current_dir, self.filetree, line)
        self.update_tree()

    def complete_mv(self, text, line, begidx, endidx):
        completions = self.autocomplete(text, line, begidx, endidx)
        return completions

    def do_rm(self, line):
        line = self.join_command_to_line("rm", line)
        shell_command(self.current_dir, self.filetree, line)
        self.update_tree()

    def complete_rm(self, text, line, begidx, endidx):
        completions = self.autocomplete_dir(text, line, begidx, endidx)
        return completions

    def do_cp(self, line):
        line = self.join_command_to_line("cp", line)
        shell_command(self.current_dir, self.filetree, line)
        self.update_tree()

    def complete_cp(self, text, line, begidx, endidx):
        completions = self.autocomplete_dir(text, line, begidx, endidx)
        return completions

    def do_passwd(self, line):
        line = self.join_command_to_line("passwd", line)
        shell_command(self.current_dir, self.filetree, line)
        self.update_tree()

    def complete_passwd(self, text, line, begidx, endidx):
        completions = self.autocomplete_dir(text, line, begidx, endidx)
        return completions

    def do_xargs(self, line):
        line = self.join_command_to_line("xargs", line)
        shell_command(self.current_dir, self.filetree, line)

    def do_cat(self, line):
        line = self.join_command_to_line("cat", line)
        shell_command(self.current_dir, self.filetree, line)

    def complete_cat(self, text, line, begidx, endidx):
        completions = self.autocomplete(text, line, begidx, endidx)
        return completions

    def do_sudo(self, line):
        line = self.join_command_to_line("sudo", line)
        sudo(self.current_dir, self.filetree, line)

    def do_clear(self, line):
        line = self.join_command_to_line("clear", line)
        shell_command(self.current_dir, self.filetree, line)

    #######################################################
    # Commands that do not use piping when using subprocess

    def do_nano(self, line):
        line = self.join_command_to_line("nano", line)
        launch_application(self.current_dir, self.filetree, line)

    def complete_nano(self, text, line, begidx, endidx):
        completions = self.autocomplete_dir(text, line, begidx, endidx)
        return completions

    # Tis is listed with the other launched applications because
    # the piping only works if no piping is used
    def do_echo(self, line):
        line = self.join_command_to_line("echo", line)
        launch_application(self.current_dir, self.filetree, line)

    def do_man(self, line):
        line = self.join_command_to_line("man", line)
        launch_application(self.current_dir, self.filetree, line)

    def do_less(self, line):
        line = self.join_command_to_line("less", line)
        launch_application(self.current_dir, self.filetree, line)

    def do_more(self, line):
        line = self.join_command_to_line("more", line)
        launch_application(self.current_dir, self.filetree, line)

    #######################################################
    # Helper commands

    def autocomplete_dir(self, text, line, begidx, endidx):
        temp_dir = get_completion_dir(self.current_dir, self.filetree, line)
        autocomplete_list = list(self.filetree.show_direct_descendents(temp_dir))
        completions = []
        if not text:
            completions = autocomplete_list[:]
        else:
            for f in autocomplete_list:
                if f.startswith(text):
                    completions.append(f)
            if len(completions) == 1:
                if self.filetree[completions[0]].is_dir:
                    completions[0] += "/"

        return completions

    def autocomplete(self, text, line, begidx, endidx, complete_list):
        if not text:
            completions = complete_list[:]
        else:
            completions = [f
                           for f in complete_list
                           if f.startswith(text)
                           ]
        return completions

    def join_command_to_line(self, command_word, line):
        line = " ".join([command_word] + line.split(" "))
        return line


def launch_project(terminal_number=None):
    filepath = dir_path + "/linux_story/data/challenges.json"
    file_contents = ""
    with open(filepath) as infile:
        file_contents = infile.read().strip()
    challenges = json.loads(file_contents)

    if terminal_number:
        launch_challenge_number(terminal_number, challenges)

    for i in range(1, NUMBER_OF_CHALLENGES):
        launch_challenge_number(i, challenges)


def launch_challenge_number(terminal_number, challenges):
    challenge_dict = challenges[str(terminal_number)]
    for line in challenge_dict["story"]:
        line = colourizeInput256(line, 147, 16, True)
        try:
            raw_input(line)
        except:
            pass

    # if there's animation, play it
    try:
        animation_cmd = challenge_dict["animation"]
        launch_animation(animation_cmd)
    except:
        # fail silently
        pass

    start_dir = challenge_dict["start_dir"]
    end_dir = challenge_dict["end_dir"]
    command = challenge_dict["command"]
    hint = challenge_dict["hint"]
    copy_file_tree(terminal_number)
    Terminal(start_dir, end_dir, command, hint)


def launch_animation(command):
    # split the command into it's components
    elements = command.split(" ")

    # the filename is the first element
    filename = elements[0]

    # find complete path
    path = os.path.join(os.path.join(os.path.dirname(__file__), "animation", filename))

    # join command back up
    command = " ".join([path] + elements[1:])

    # run command
    os.system(command)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        launch_project(sys.argv[1])
    else:
        launch_project()
