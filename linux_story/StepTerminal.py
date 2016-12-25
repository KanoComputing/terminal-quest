import os
from cmd import Cmd

import readline

from linux_story.IStep import IStep
from linux_story.common import fake_home_dir, get_username, tq_file_system
from linux_story.dependencies import get_app_xp_for_challenge, translate
from linux_story.file_creation.FileTree import FileTree
from linux_story.helper_functions import colour_string_with_preset
from linux_story.load_defaults_into_filetree import delete_item


class StepTerminal(Cmd, IStep):
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

    def __init__(self, message_client, location, xp=""):
        Cmd.__init__(self)

        self.__message_client = message_client
        self.__location = location

        # Initialise the Step stuff first
        self.__xp = xp
        self.__command_blocked = False

        # Currently this is passed to the Terminal class but NOT updated because we're making a copy.
        self.last_cmd_output = ""

        # Last command user tried to run.
        self.last_user_input = ""

        # self.current_path is the current path that the user sees
        self.__current_path = self.start_dir

        if not self.dirs_to_attempt:
            self.dirs_to_attempt = self.start_dir

        self.__delete_items()
        self.__modify_file_tree()
        self.__setup_cmd()

    def is_finished(self, line):
        finished = self.__finished_challenge(line)
        return self._client.finish_if_server_ready(finished)

    def __finished_challenge(self, line):
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

    def run(self):
        self.__send_start_challenge_data()
        self.cmdloop()

    def next_step(self):
        pass

    def send_xp_info(self):
        xp = get_app_xp_for_challenge("linux-story", str(self.challenge_number))
        if xp > 0:
            self.__xp = translate("{{gb:Congratulations, you earned %d XP!}}\n\n") % xp

    def __send_start_challenge_data(self):
        """Sends all the relevent information at the start of a new step
        """
        coloured_username = "{{yb:" + get_username() + ":}} "
        print_text = "\n".join(self.print_text)

        if print_text:
            print_text = coloured_username + print_text

        self.__message_client.send_start_challenge_data(
            "\n".join(self.story),
            str(self.challenge_number),
            self.terminal_commands,
            self.highlighted_commands,
            self.__xp,
            print_text
        )

    def __get_real_path(self):
        return self.__generate_real_path(self.__current_path)

    @staticmethod
    def __generate_real_path(fake_path):
        return fake_path.replace('~', fake_home_dir)

    @staticmethod
    def __generate_fake_path(real_path):
        return real_path.replace(fake_home_dir, '~')

    def __set_prompt(self):
        fake_cwd = self.__get_real_path().replace(fake_home_dir, '~')

        if fake_cwd[-1] == '/':
            fake_cwd = fake_cwd[:-1]

        username = get_username()
        yellow_part = username + "@kano "
        yellow_part = colour_string_with_preset(yellow_part, "yellow", True)

        blue_part = fake_cwd + ' $ '
        blue_part = colour_string_with_preset(blue_part, "blue", True)

        # self.prompt inherited from Cmd
        self.prompt = yellow_part + blue_part

    def __setup_cmd(self):
        # This changes the special characters, so we can autocomplete on the - character
        old_delims = readline.get_completer_delims()
        readline.set_completer_delims(old_delims.replace('-', ''))

        self.__set_prompt()

    def __delete_items(self):
        if self.deleted_items:
            for path in self.deleted_items:
                real_path = os.path.expanduser(path.replace('~', fake_home_dir))
                delete_item(real_path)

    def __modify_file_tree(self):
        if self.file_list:
            file_tree = FileTree(None, tq_file_system)
            for f in self.file_list:
                if "type" in f and f["type"] == "file":
                    file_tree.create_item(f["type"], f["path"], f["permissions"], f["contents"])
                else:
                    file_tree.create_item(f["type"], f["path"], f["permissions"], "")