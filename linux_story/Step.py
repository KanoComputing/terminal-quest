#!/usr/bin/env python

# Step.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Step class to describe the flow

import time
import threading
import ast
import os
from socket_functions import launch_client, is_server_busy
from kano_profile.badges import save_app_state_variable_with_dialog
from kano_profile.apps import (
    load_app_state_variable, get_app_xp_for_challenge
)
from load_defaults_into_filetree import delete_item, modify_file_tree


class Step():
    story = [""]
    start_dir = "~"
    end_dir = "~"
    commands = ""
    hints = ""
    last_step = False
    challenge_number = ""
    output_condition = lambda x, y: False
    story_dict = {}
    deleted_items = []
    xp = ""
    SAVING_NANO_PROMPT = "Save modified buffer (ANSWERING \"No\" WILL DESTROY CHANGES) ? "
    SAVE_FILENAME = "File Name to Write"

    # We can either tree as a global variable in common, or pass it as a
    # variable between the files.
    # We have to be careful with tree, as it has to be accessed from the right
    # thread otherwise the old data is erased.
    def __init__(self, Terminal_Class, xp=""):

        self.xp = xp
        self.pipe_busy = False
        self.nano_running = False
        self.nano_content = ""
        self.last_nano_prompt = ""
        self.ctrl_x = False
        self.on_nano_filename_screen = False
        self.exited_nano = True
        self.nano_x = 0
        self.nano_y = 0
        self.last_cmd_output = None
        self.fake_path = self.start_dir
        self.save_prompt_showing = False
        self.nano_filename = ""

        self.modify_file_tree()
        self.delete_items()

        # Available commands that can be used in the Terminal
        self.terminal_commands = Terminal_Class.commands

        # if hints are a string
        if isinstance(self.hints, basestring):
            self.hints = [self.hints]

        self.terminal = Terminal_Class(
            self.start_dir,
            self.end_dir,
            self.check_command,
            self.block_command,
            self.check_output,
            self.last_cmd_output,
            self.fake_path,

            # Because of this, we may not need
            # self.check_command and self.check_output
            self.finished_challenge,

            self.get_nano_contents,
            self.set_nano_running
        )

        self.run()

    def run(self):
        '''Runs through the Step, which does the following:
        - Displays the challenge number at the top
        - Types out the story
        - Creates the new personalised Terminal with the available commands
        - Once the terminal exits, takes you to the next Step
        '''

        # Save the challenge information on run.
        # We would save on every step, but it's a little too
        # slow to do this since save_app_state_variable refreshes kdesk

        # Send all story data together
        self.send_start_challenge_data()

        self.launch_terminal()

        if self.last_step:
            self.save_challenge()

        # Tell storyline the step is finished
        self.next()

    def exit(self):
        data = {'exit': '1'}
        t = threading.Thread(target=launch_client, args=(data,))
        t.daemon = True
        t.start()

    def send_text(self, string):
        '''Sends a string through the pipe to the GUI
        '''

        if not is_server_busy():
            data = {'hint': string}
            t = threading.Thread(target=launch_client, args=(data,))
            t.daemon = True
            t.start()

    def send_hint(self, hint=None):
        '''Sends a hint string through the pipe to the GUI
        '''

        if not is_server_busy():
            if not hint:
                hint = '\n' + self.hints[0]
            else:
                hint = '\n' + hint
            data = {'hint': hint}
            t = threading.Thread(target=launch_client, args=(data,))
            t.daemon = True
            t.start()

    def send_start_challenge_data(self):
        '''Sends all the relevent information at the start of a new step
        '''

        data = {}

        # Get data about any XP.
        data['xp'] = self.xp
        data['story'] = "\n".join(self.story)
        data['challenge'] = str(self.challenge_number)
        data['spells'] = self.terminal_commands

        t = threading.Thread(target=launch_client, args=(data,))
        t.daemon = True
        t.start()

    def next(self):
        '''Defines what should happen next at the end of this step
        Should be modified on inheritance
        '''

        pass

    def delete_items(self):
        '''self.delete_items should be a list of fake_paths we want removed
        '''
        if self.deleted_items:
            for path in self.deleted_items:

                # TODO: move this to common
                real_path = os.path.expanduser(path.replace('~', '~/.linux-story'))
                delete_item(real_path)

    def get_xp(self):
        '''Look up XP earned after challenge
        '''
        # Look up XP earned
        xp = get_app_xp_for_challenge("linux-story",
                                      str(self.challenge_number)
                                      )

        if xp > 0:
            self.xp = "{{gb:Congratulations, you earned " + str(xp) + " XP!}}\n\n"

    def save_challenge(self):
        '''Integration with kano world
        '''
        level = load_app_state_variable("linux-story", "level")

        if self.challenge_number > level:
            save_app_state_variable_with_dialog("linux-story", "level",
                                                self.challenge_number)
            self.get_xp()

    def launch_terminal(self):
        '''Starts off the terminal's game loop.
        This function does not stop until the user has passed the level
        '''

        self.terminal.cmdloop()

    def check_command(self, line, current_dir):
        '''If self.commands is provided, checks the command entered
        by the user matches self.commands.
        '''

        # check through list of commands
        command_validated = True
        end_dir_validated = True

        # strip any spaces off the beginning and end
        line = line.strip()

        # if the validation is included
        if self.commands:
            # if only one command can pass the level
            if isinstance(self.commands, basestring):
                command_validated = line == self.commands
            # else there are multiple commands that can pass the level
            else:
                command_validated = line in self.commands

        if self.end_dir:
            end_dir_validated = current_dir == self.end_dir

        if not (command_validated and end_dir_validated):
            self.show_hint(line, current_dir)

        condition = (command_validated and end_dir_validated)
        return self.finish_if_server_ready(condition)

    def finish_if_server_ready(self, other_condition):
        return self.terminal.finish_if_server_ready(other_condition)

    def show_hint(self, line, current_dir):
        '''Customize the hint that is shown to the user
        depending on their input
        '''
        # Default behaviour
        # if user does not pass challenge, show hints.
        # Go through hints until we get to last hint
        # then just keep showing last hint
        self.send_hint()

        if len(self.hints) > 1:
            self.hints.pop(0)

    def block_command(self, line):
        '''line is the user entered input from the terminal.
        If this function returns True, input entered will be blocked
        Otherwise, command will be run as normal.
        Default behaviour is to block cd and mv
        '''

        line = line.strip()
        if "cd" in line or "mkdir" in line or \
                ("mv" in line and not line == 'mv --help'):

            print ('Nice try! But you do not need that command for this '
                   'challenge')

            return True

    def check_output(self, output):
        '''Use output of the command to level up.
        The argument is the output from the command printed in the terminal.
        If the function return True, will break out of cmdloop and go to next
        Step.
        if the function returns False, whether the level passes depends on
        the return value of self.check_command
        '''
        if not output:
            return False

        output = output.strip()
        return self.output_condition(output)

    def finished_challenge(self, line):
        '''If this returns True, we exit the cmdloop.
        If this return False, we stay in the cmdloop.

        Depending on the challenge, we may want to either pass only
        depending on the output, but not on the command.  So we may want
        to change this in an instance of the Step class.
        '''

        finished = self.check_output(self.last_cmd_output) or \
            self.check_command(line, self.fake_path)

        return finished

    def modify_file_tree(self):
        '''If self.story_dict is specified, add files to the filetree
        '''
        if self.story_dict:
            modify_file_tree(self.story_dict)

    ##################################################################
    # nano functions

    def set_nano_running(self, nano_running):
        '''Set this while nano is running
        '''
        self.nano_running = nano_running

    def get_nano_running(self):
        return self.nano_running

    def quit_nano(self):
        self.cancel_everything()
        self.set_nano_running(False)

    def set_nano_content(self, nano_content):
        '''Setter for the self.nano_content for this Step
        '''
        self.nano_content = nano_content

    def get_nano_content(self):
        '''Getter for the self.nano_content for this Step
        '''
        return self.nano_content

    def check_nano_content(self):
        '''These can be updated by the individual Step instances
        to do something with the changed values
        '''
        # Do something with the self.nano_content
        pass

    def set_nano_x(self, x):
        '''These can be updated by the individual Step instances
        to do something with the changed values
        '''
        self.nano_x = x

    def set_nano_y(self, y):
        '''These can be updated by the individual Step instances
        to do something with the changed values
        '''
        self.nano_y = y

    def set_ctrl_x_nano(self, ctrl_x):
        '''Setting whether the user pressed Ctrl X.
        ctrl_x is a bool.
        '''
        self.ctrl_x = ctrl_x

    def get_ctrl_x_nano(self):
        '''Getting whether the user pressed Ctrl X.
        '''
        return self.ctrl_x

    def set_last_prompt(self, last_prompt):
        '''Save last prompt.  This means we can see what the response
        is responding to.
        '''
        self.last_nano_prompt = last_prompt

    def set_on_filename_screen(self, on_filename_screen):
        self.on_nano_filename_screen = on_filename_screen

    def get_on_filename_screen(self):
        return self.on_nano_filename_screen

    def get_last_prompt(self):
        return self.last_nano_prompt

    def set_nano_content_values(self, content_dict):
        '''Set the x, y coordinates and the content.
        content_dict = {'x': 1, 'y': 2, 'text': ['line1', 'line2']}
        '''
        self.set_nano_x(content_dict["x"])
        self.set_nano_x(content_dict["y"])
        nano_content = "\n".join(content_dict["text"])
        self.set_nano_content(nano_content)
        self.set_save_prompt_showing(False)

    def cancel_everything(self):
        '''If the response of any prompt or statusbar is Cancel,
        then everything should be set to False
        '''
        self.set_save_prompt_showing(False)
        self.set_ctrl_x_nano(False)
        self.set_on_filename_screen(False)

    def set_save_prompt_showing(self, showing):
        self.save_prompt_showing = showing

    def get_save_prompt_showing(self):
        return self.save_prompt_showing

    def set_nano_filename(self, filename):
        self.nano_filename = filename

    def get_nano_filename(self):
        return self.nano_filename

    def get_nano_contents(self):
        pipename = "/tmp/linux-story-nano-pipe"
        if not os.path.exists(pipename):
            open(pipename, 'w+').close()

        f = open(pipename)

        while self.get_nano_running():
            time.sleep(0.1)
            line = None

            for line in iter(f.readline, ''):

                # Assuming we're receiving something of the form
                # {x: 1, y: 1, text: ["line1", "line2"]}
                # {response: this is the response message}

                data = ast.literal_eval(line)

                if "contents" in data:
                    self.cancel_everything()
                    value = data["contents"]

                    if self.get_nano_content() != self.end_text:
                        self.set_nano_content_values(value)

                if "statusbar" in data:
                    value = data["statusbar"]
                    # Everything is set to False, since anything could
                    # have been cancelled
                    if value.strip().lower() == "cancelled":
                        self.cancel_everything()

                if "response" in data:
                    value = data["response"]
                    # If the last prompt is the saving nano buffer prompt,
                    # then the user has tried to exit without saving
                    # his/her work.

                    if self.get_last_prompt() == self.SAVING_NANO_PROMPT:
                        if value.lower() == "cancel":
                            self.cancel_everything()

                        elif value.lower() == "yes":
                            # Starting to save.
                            # Bring up the relevent prompt about entering
                            # the filename and pressing Y.
                            # Set variable that says the player is on this
                            # screen
                            self.set_save_prompt_showing(True)
                            self.set_on_filename_screen(True)

                        elif value.lower() == "no":
                            # Exited nano and chose not to save
                            # This may not need to be recorded.
                            self.quit_nano()

                    elif self.get_last_prompt() == self.SAVE_FILENAME:
                        if value.lower() == "no":
                            self.quit_nano()
                        elif value.lower() == "cancel":
                            self.cancel_everything()

                        # TODO: not sure this is needed
                        elif value.lower() == "aborted enter":
                            self.cancel_everything()

                if "prompt" in data:
                    value = data["prompt"]
                    self.set_last_prompt(value)

                    if value == self.SAVE_FILENAME:
                        self.set_save_prompt_showing(False)
                        self.set_on_filename_screen(True)

                    # Do we set anything here?
                    elif value == self.SAVING_NANO_PROMPT:
                        self.set_save_prompt_showing(True)
                        self.set_on_filename_screen(False)

                if "saved" in data:
                    self.set_nano_filename(data["filename"])

                if "finish" in data:
                    self.quit_nano()

            else:
                if line:
                    # Run a check for self.nano_content.
                    # If this returns True, break out of the loop.
                    if self.check_nano_content():
                        return

    def check_nano_has_been_saved(self, file_contents, file_name):
        '''
        To check nano has been saved correctly:
        - Check the filepath exists.
        - That the file contains the correct contents.
        '''
        pass
