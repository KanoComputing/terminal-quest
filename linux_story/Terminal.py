# Terminal.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The template of the terminal classes.


import os
import sys
from cmd import Cmd

from linux_story.file_creation.FileTree import FileTree

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from helper_functions import (
    get_script_cmd, is_exe, colour_string_with_preset
)
from linux_story.dependencies import load_app_state_variable, save_app_state_variable_with_dialog, \
    get_app_xp_for_challenge, Logger, translate
from linux_story.MessageClient import MessageClient
from common import get_username, fake_home_dir, tq_file_system
from load_defaults_into_filetree import delete_item, modify_file_tree
from linux_story.commands_real import run_executable
import strings

# If this is not imported, the escape characters used for the colour prompts
# show up as special characters.
import readline


class Terminal(Cmd):
    terminal_commands = []
    highlighted_commands = []
    print_text = [""]
    story = [""]
    start_dir = "~"
    dirs_to_attempt = ""
    end_dir = "~"
    commands = ""
    hints = ""
    last_step = False
    challenge_number = ""
    output_condition = lambda x, y: False
    story_dict = {}
    deleted_items = []
    file_list = []
    command_blocked = False
    needs_sudo = False

    # Trying to merge Step and Terminal
    def __init__(self, xp=""):

        ##################################
        # Initialise the Step stuff first
        self.xp = xp
        self.pipe_busy = False

        # Currently this is passed to the Terminal class but NOT updated because we're making a copy.
        self.last_cmd_output = ""

        # Last command user tried to run.
        self.last_user_input = ""

        # self.current_path is the current path that the user sees
        self.current_path = self.start_dir

        if not self.dirs_to_attempt:
            self.dirs_to_attempt = self.start_dir

        # real_path is the actual filename.
        self.real_path = self.generate_real_path(self.current_path)

        self.delete_items()
        self.modify_file_tree()

        # if hints are a string
        if isinstance(self.hints, basestring):
            self.hints = [self.hints]

        self._client = MessageClient()

        ##################################

        Cmd.__init__(self)

        # This changes the special characters, so we can autocomplete on the - character
        old_delims = readline.get_completer_delims()
        readline.set_completer_delims(old_delims.replace('-', ''))

        self.set_prompt()
        self.send_start_challenge_data()

        # Need to call .cmdloop() to start terminal class.
        self.cmdloop()

        # Once the Terminal has finished, decide whether to add xp to profile
        if self.last_step:
            self.save_challenge()

        self.next()

    def generate_real_path(self, fake_path):
        return fake_path.replace('~', fake_home_dir)

    def generate_fake_path(self, real_path):
        return real_path.replace(fake_home_dir, '~')

    def set_prompt(self):
        fake_cwd = self.real_path.replace(fake_home_dir, '~')

        if fake_cwd[-1] == '/':
            fake_cwd = fake_cwd[:-1]

        username = get_username()
        yellow_part = username + "@kano "
        yellow_part = colour_string_with_preset(yellow_part, "yellow", True)

        blue_part = fake_cwd + ' $ '
        blue_part = colour_string_with_preset(blue_part, "blue", True)
        self.prompt = yellow_part + blue_part

    def emptyline(self):
        """To overwrite default behaviour in the cmd module.
        Do nothing if the user enters an empty line.
        """
        pass

    def do_shell(self, line):
        """This is run by default if the line starts with !.
        """
        # We use this over os.system so that the command is run in the
        # correct directory
        run_executable(self.real_path, line)

    def precmd(self, line):
        """Hook before the command is run
        If the self.block_command returns True, the command is not run
        Otherwise, it is run
        """

        self.last_user_input = line.strip()

        if self.block_command():
            self.set_command_blocked(True)
            return Cmd.precmd(self, "")
        else:
            self.set_command_blocked(False)
            return Cmd.precmd(self, line)

    def onecmd(self, line):
        """Modified Cmd.cmd.onecmd so that it can detect if a file is a script,
        and can run it appropriately

        Keyword arguments:
        line - string.  Is what the user enters at the terminal

        Check if value entered is a shell script
        """

        is_script, script = get_script_cmd(
            line,
            self.real_path
        )
        if is_script:
            self.do_shell(line)
        else:
            self.last_cmd_output = Cmd.onecmd(self, line)
            return self.last_cmd_output

    def postcmd(self, stop, line):
        """If the command output is correct, or if the command typed is
        correct, then return True
        Returning True exits the cmdloop() function
        """

        finished = self.finished_challenge(line)
        return self._client.finish_if_server_ready(finished)


    #######################################################
    # Step functions for levelling up

    def next(self):
        """Defines what should happen next at the end of this step
        Should be modified on inheritance
        """
        pass

    def block_command(self):
        """
        If this function returns True, the last input (self.last_user_input)
        will be blocked.
        Otherwise, command will be run as normal.
        Default behaviour is to block cd, mv and mkdir.
        """

        return self.default_block_command()

    def default_block_command(self):
        if "cd" in self.last_user_input or \
                "mkdir" in self.last_user_input or \
                ("mv" in self.last_user_input and
                    not self.last_user_input == 'mv --help'):

            print strings.COMMAND_BLOCKED_MESSAGE
            return True

        return False

    def check_output(self, output):
        """Use output of the command to level up.
        The argument is the output from the command printed in the terminal.
        If the function return True, will break out of cmdloop and go to next
        Step.
        if the function returns False, whether the level passes depends on
        the return value of self.check_command
        """
        if not output:
            return False

        output = output.strip()
        return self.output_condition(output)

    def finished_challenge(self, line):
        """If this returns True, we exit the cmdloop.
        If this return False, we stay in the cmdloop.

        Depending on the challenge, we may want to either pass only
        depending on the output, but not on the command.  So we may want
        to change this in an instance of the Step class.
        """
        finished = self.check_output(self.last_cmd_output) or \
            self.check_command()

        return finished

    def check_command(self):
        """If self.commands is provided, checks the command entered
        by the user matches self.commands.
        """

        return self._default_check_command()

    def _default_check_command(self):
        command_validated = self._validate_check_command()
        end_dir_validated = self._validate_end_dir()
        if not (command_validated and end_dir_validated):
            self.send_hint()
        return self._client.finish_if_server_ready((command_validated and end_dir_validated))

    def _validate_check_command(self):
        command_validated = True
        # if the validation is included
        if self.commands:
            # if only one command can pass the level
            if isinstance(self.commands, basestring):
                command_validated = (self.last_user_input == self.commands)
            # else there are multiple commands that can pass the level
            else:
                command_validated = self.last_user_input in self.commands
        return command_validated

    def _validate_end_dir(self):
        end_dir_validated = True
        if self.end_dir:
            end_dir_validated = self.current_path == self.end_dir
        return end_dir_validated

    #######################################################
    # Send text to the GUI.

    def send_hint(self, hint=None):
        """Sends a hint string through the pipe to the GUI
        """

        if not hint:
            hint = '\n' + self.hints[0]
        else:
            hint = '\n' + hint
        self._client.send_hint(hint)

        # TODO: This should only be run is a hint is not provided
        if len(self.hints) > 1:
            self.hints.pop(0)

    def send_text(self, string):
        """Sends a string through the pipe to the GUI
        """
        self._client.send_hint(string)

    def send_start_challenge_data(self):
        """Sends all the relevent information at the start of a new step
        """
        coloured_username = "{{yb:" + get_username() + ":}} "
        print_text = "\n".join(self.print_text)

        if print_text:
            print_text = coloured_username + print_text

        self._client.send_start_challenge_data(
            "\n".join(self.story),
            str(self.challenge_number),
            self.terminal_commands,
            self.highlighted_commands,
            self.xp,
            print_text
        )

    def send_dark_theme(self):
        self._client.set_dark_theme()

    def send_normal_theme(self):
        self._client.set_normal_theme()

    def get_xp(self):
        """Look up XP earned after challenge
        """
        xp = get_app_xp_for_challenge("linux-story", str(self.challenge_number))
        if xp > 0:
            self.xp = translate("{{gb:Congratulations, you earned %d XP!}}\n\n") % xp

    def exit(self):
        self._client.exit()

    ######################################################
    # Kano world integration

    def save_challenge(self):
        """Integration with kano world
        """
        level = load_app_state_variable("linux-story", "level")

        if self.challenge_number > level:
            save_app_state_variable_with_dialog("linux-story", "level", self.challenge_number)
            self.get_xp()

    #######################################################
    # File system functions

    def delete_items(self):
        """self.deleted_items should be a list of fake_paths we want removed
        """
        if self.deleted_items:
            for path in self.deleted_items:
                real_path = os.path.expanduser(path.replace('~', fake_home_dir))
                delete_item(real_path)

    def modify_file_tree(self):
        """If self.story_dict is specified, add files to the filetree
        """
        if self.file_list:
            file_tree = FileTree(None, tq_file_system)
            for f in self.file_list:
                if "type" in f and f["type"] == "file":
                    file_tree.create_item(f["type"], f["path"], f["permissions"], f["contents"])
                else:
                    file_tree.create_item(f["type"], f["path"], f["permissions"], "")
    #######################################################
    # Helper commands

    def autocomplete_files(self, text, line, begidx, endidx, only_dirs=False,
                           only_exe=False):

        try:
            additional_path = line[:int(begidx)].split(" ")[-1]

            # If we do ls ~/ we need to change the path to be absolute.
            if additional_path.startswith('~'):
                # Needs to be moved to helper_functions
                additional_path = additional_path.replace('~', fake_home_dir)
                path = os.path.expanduser(additional_path)
            else:
                path = os.path.join(self.real_path, additional_path)

            if not os.path.exists(path):
                return []

            if text == "..":
                completions = [text]
            elif not text and line == "./":
                # This is repeated
                contents = os.listdir(path)
                completions = [f
                               for f in contents
                               if f.startswith(text) and (
                                   os.path.isdir(os.path.join(path, f)) or
                                   is_exe(os.path.join(path, f)))
                               ]
            elif not text:
                completions = os.listdir(path)
            else:
                contents = os.listdir(path)

                if only_dirs:
                    completions = [f
                                   for f in contents
                                   if f.startswith(text) and
                                   os.path.isdir(os.path.join(path, f))
                                   ]
                elif only_exe:
                    completions = [f
                                   for f in contents
                                   if f.startswith(text) and (
                                       os.path.isdir(os.path.join(path, f)) or
                                       is_exe(os.path.join(path, f)))
                                   ]
                else:
                    completions = [f
                                   for f in contents
                                   if f.startswith(text)
                                   ]

            if len(completions) == 1 and \
                    os.path.isdir(os.path.join(path, completions[0])):
                completions = [completions[0] + '/']

            return completions

        except Exception as e:
            Logger.debug("Hit Exception in the autocomplete_files function {}".format(str(e)))

    # Overwrite this to check for shell scripts instead.
    def completedefault(self, *ignored):
        """ignored = [text, line, begidx, endidx]
        text = (string I think?) ?
        line = (string) line the user entered
        begidx = (int) ?
        endidx = (int) ?
        """
        [text, line, begidx, endidx] = ignored
        return self.autocomplete_files(
            text, line, begidx, endidx, only_exe=True
        )

    def complete_executable(self, text, line, begidx, endidx):
        # Asssuming the input is of the form.
        return ["./"]

    # The original text from the cmd module.
    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """

        if state == 0:
            import readline
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped
            if begidx > 0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
            else:
                # Modified this so we check for executables sometimes
                if line == ".":
                    compfunc = self.complete_executable
                else:
                    compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    #######################################################
    # Set whether command has been blocked

    def set_command_blocked(self, blocked):
        self.command_blocked = blocked

    def get_command_blocked(self):
        return self.command_blocked
