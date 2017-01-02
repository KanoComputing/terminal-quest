# terminal_nano.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges


import os
import threading

from kano.logging import logger

from linux_story.PlayerLocation import generate_real_path
from linux_story.commands_real import nano
from linux_story.story.new_terminals.terminal_mkdir import TerminalMkdir


class TerminalNano(TerminalMkdir):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo", "mkdir", "nano"]

    def __init__(self, step, location, dirs_to_attempt):
        self._step_nano = step.get_nano_logic()

        TerminalMkdir.__init__(self, step, location, dirs_to_attempt)

    def do_nano(self, line):

        ##########################################
        # set up step_nano
        self._step_nano.set_nano_running(True)
        self._step_nano.opened_nano(line)

        # Read contents of the file
        text = self.read_goal_contents()
        self._step_nano.set_nano_content(text)
        ##########################################

        # Read nano in a separate thread
        t = threading.Thread(target=self.try_and_get_pipe_contents)
        t.daemon = True
        t.start()

        # If the line is given, it is the filepath of the file we are
        # adjusting.
        # if line:
        #    self.set_last_nano_filepath(line)

        nano(self._location.get_real_path(), line)

    def try_and_get_pipe_contents(self):
        try:
            self._step_nano.get_pipe_contents()
        except Exception as e:
            logger.error(
                "\nFailed to get nano contents, exception {}".format(str(e))
            )
            self._step.send_hint("\nFailed to get nano contents, {}".format(str(e)))

    def read_goal_contents(self):
        text = ""
        end_path = generate_real_path(self._step_nano.get_goal_nano_filepath())

        if os.path.exists(end_path):
            # check contents of file contains the self.end_text
            f = open(end_path, "r")
            text = f.read()
            f.close()

        return text