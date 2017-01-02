

from linux_story.PlayerLocation import PlayerLocation
from linux_story.common import get_username
from linux_story.file_creation.FileTree import delete_items
from linux_story.file_creation.FileTree import modify_file_tree
from linux_story.helper_functions import record_user_interaction
from linux_story.story.StepNano import StepNano


class IStep:
    highlighted_commands = []
    print_text = None
    story = [""]
    start_dir = "~"
    dirs_to_attempt = [""]
    end_dir = "~"
    commands = ""
    hints = [""]
    output_condition = lambda x, y: False
    deleted_items = None
    file_list = None
    TerminalClass = None
    prev_command = ""
    companion_speech = ""
    companion_command = ""

    def __init__(self, client):
        self._run_at_start()
        self._nano = StepNano()
        self._setup_nano()
        self.__modify_file_system()

        if isinstance(self.hints, basestring):
            raise Exception("Hint is a string! Bad Caroline!")

        self._client = client
        self._location = PlayerLocation(self.start_dir, self.end_dir)
        self._last_user_input = ""
        self._is_finished = False
        self.__command_blocked = False

    def _run_at_start(self):
        # Hook to run at start
        pass

    def _setup_nano(self):
        # override and set nano values in here.
        pass

    def __modify_file_system(self):
        delete_items(self.deleted_items)
        modify_file_tree(self.file_list)

    def run(self):
        self.TerminalClass(self, self._location, self.dirs_to_attempt).cmdloop()

    def next(self):
        raise Exception("IStep method not implemented")

    def is_finished_step(self, last_user_input, last_cmd_output):
        return self.check_output(last_cmd_output) or self.check_command(last_user_input)

    def block_command(self, last_user_input):
        pass

    def check_command(self, last_user_input):
        return self._default_check_command(last_user_input)

    def check_output(self, output):
        if not output:
            return False

        output = output.strip()
        return self.output_condition(output)

    def set_last_user_input(self, last_user_input):
        self._last_user_input = last_user_input

    def get_location(self):
        return self._location

    def is_finished_game(self):
        return self._is_finished

    def _is_at_end_dir(self):
        return self._location.is_at_end_dir()

    def get_fake_path(self):
        return self._location.get_fake_path()

    def _default_check_command(self, last_user_input):
        command_validated = self._validate_check_command(last_user_input)
        end_dir_validated = self._validate_end_dir()
        if not (command_validated and end_dir_validated):
            self.send_stored_hint()
        return self._client.finish_if_server_ready((command_validated and end_dir_validated))

    def _validate_check_command(self, last_user_input):
        command_validated = True
        if self.commands:
            if isinstance(self.commands, basestring):
                command_validated = (last_user_input == self.commands)
            else:
                command_validated = last_user_input in self.commands
        return command_validated

    def _validate_end_dir(self):
        end_dir_validated = True
        if self.end_dir:
            end_dir_validated = self._location.get_fake_path() == self.end_dir
        return end_dir_validated

    def send_stored_hint(self):
        self._client.send_hint('\n' + self.hints[0])
        if len(self.hints) > 1:
            self.hints.pop(0)

    def send_hint(self, string):
        self._client.send_hint('\n' + string)

    def send_dark_theme(self):
        self._client.set_dark_theme()

    def send_normal_theme(self):
        self._client.set_normal_theme()

    def get_print_text(self):
        print_text = ""

        if self.print_text:
            coloured_username = "{{yb:" + get_username() + ":}} "
            print_text = coloured_username + "\n".join(self.print_text)

        return print_text

    def exit(self):
        self._client.exit()

    def set_command_blocked(self, blocked):
        self.__command_blocked = blocked

    def get_command_blocked(self):
        return self.__command_blocked

    def _companion_speaks(self, line):
        if line == self.companion_command and self.companion_speech:
            self.send_hint("\n" + self.companion_speech)
            record_user_interaction(self, "_".join(self.companion_command.split(" ")))

