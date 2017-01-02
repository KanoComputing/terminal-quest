import os
from cmd import Cmd

from linux_story.commands_real import run_executable
from linux_story.common import fake_home_dir, get_username
from linux_story.dependencies import Logger
from linux_story.helper_functions import get_script_cmd, is_exe, colour_string_with_preset
import readline


class KanoCmd(Cmd):

    def __init__(self, step, location, dirs_to_attempt):
        """
        :param step: IStep type
        :param location: PlayerLocation location
        """
        Cmd.__init__(self)
        self._step = step
        self.__command_blocked = False
        self._location = location
        self._dirs_to_attempt = dirs_to_attempt
        self.last_cmd_output = ""

        self._set_prompt()
        self._autocomplete_dash_characters()

    def _set_prompt(self):
        # Why is this done like this? Can we shorten this to just use the prompt?
        fake_cwd = self._location.get_real_path().replace(fake_home_dir, '~')

        if fake_cwd[-1] == '/':
            fake_cwd = fake_cwd[:-1]

        username = get_username()
        yellow_part = username + "@kano "
        yellow_part = colour_string_with_preset(yellow_part, "yellow", True)

        blue_part = fake_cwd + ' $ '
        blue_part = colour_string_with_preset(blue_part, "blue", True)
        self.prompt = yellow_part + blue_part

    # Public methods
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
        run_executable(self._location.get_real_path(), line)

    def precmd(self, line):
        """Hook before the command is run
        If the self.block_command returns True, the command is not run
        Otherwise, it is run
        """

        self._step.set_last_user_input(line)
        if self._step.block_command(line.strip()):
            self._set_command_blocked(True)
            return Cmd.precmd(self, "")
        else:
            self._set_command_blocked(False)
            return Cmd.precmd(self, line)

    def onecmd(self, line):
        is_script, script = get_script_cmd(line,self._location.get_real_path())
        if is_script:
            self.do_shell(line)
        else:
            self.last_cmd_output = Cmd.onecmd(self, line)
            return self.last_cmd_output

    def postcmd(self, stop, line):
        return self._step.is_finished_step(line, self.last_cmd_output)

    def completedefault(self, *ignored):
        """ignored = [text, line, begidx, endidx]
        text = (string I think?) ?
        line = (string) line the user entered
        begidx = (int) ?
        endidx = (int) ?
        """
        [text, line, begidx, endidx] = ignored
        return self._autocomplete_files(text, line, begidx, endidx, only_exe=True)

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

    def get_command_blocked(self):
        return self.__command_blocked

    # Protected methods
    def _autocomplete_files(self, text, line, begidx, endidx, only_dirs=False,
                           only_exe=False):

        try:
            additional_path = line[:int(begidx)].split(" ")[-1]

            # If we do ls ~/ we need to change the path to be absolute.
            if additional_path.startswith('~'):
                # Needs to be moved to helper_functions
                additional_path = additional_path.replace('~', fake_home_dir)
                path = os.path.expanduser(additional_path)
            else:
                path = os.path.join(self._location.get_real_path(), additional_path)

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

    def _get_real_path(self):
        return self._location.get_real_path()

    def _set_command_blocked(self, blocked):
        self._step.set_command_blocked(blocked)
        self.__command_blocked = blocked

    def _autocomplete_dash_characters(self):
        # This changes the special characters, so we can autocomplete on the - character
        old_delims = readline.get_completer_delims()
        readline.set_completer_delims(old_delims.replace('-', ''))
