# ChallengeController.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from linux_story.common import tq_file_system
from kano_profile.apps import get_app_xp_for_challenge, load_app_state_variable, save_app_state_variable
from kano_profile.badges import save_app_state_variable_with_dialog
from linux_story.file_creation.FileTree import FileTree
from linux_story.launch_functions import get_step_class
from linux_story.story.trees.default_trees import tree


# noinspection PyPep8Naming
class ChallengeController:

    def __init__(self, message_client):
        self.__message_client = message_client

    def run(self, challenge=1, step=1):
        FileTree(tree, tq_file_system).parse_complete(challenge, step)
        StepClass = get_step_class(challenge, step)
        step_instance = StepClass(self.__message_client)
        self.__send_start_challenge_data(step_instance, step_instance.TerminalClass.terminal_commands, challenge)
        step_instance.run()
        (new_challenge, new_step) = step_instance.next()

        while not step_instance.is_finished_game():
            StepClass = get_step_class(new_challenge, new_step)
            step_instance = StepClass(self.__message_client)
            self.__send_start_challenge_data(step_instance, step_instance.TerminalClass.terminal_commands, new_challenge)
            self.__save_challenge(new_challenge, challenge)
            challenge = new_challenge
            step_instance.run()
            (new_challenge, new_step) = step_instance.next()

    def __run_step(self, StepClass, challenge):
        step_instance = StepClass(self.__message_client)
        self.__send_start_challenge_data(step_instance, step_instance.TerminalClass.terminal_commands, challenge)
        step_instance.run()
        (new_challenge, new_step) = step_instance.next()
        return new_challenge, new_step, step_instance

    @staticmethod
    def __save_challenge(new_challenge, challenge):
        if new_challenge > challenge or not new_challenge:
            level = load_app_state_variable("linux-story", "level")
            if challenge > level:
                save_app_state_variable_with_dialog("linux-story", "level", challenge)

    def __send_start_challenge_data(self, step_instance, terminal_commands, challenge_number):
        self.__message_client.send_start_challenge_data(
            "\n".join(step_instance.story),
            str(challenge_number),
            terminal_commands,  # get list of commands from Cmd
            step_instance.highlighted_commands,
            self.__get_xp(challenge_number),
            step_instance.get_print_text()
        )

    @staticmethod
    def __get_xp(challenge):
        level = load_app_state_variable("linux-story", "level")
        if level is None:
            save_app_state_variable("linux-story", "level", 0)
            return ""

        if challenge > level + 1:
            xp = get_app_xp_for_challenge("linux-story", str(challenge))
            if xp > 0:
                return _("{{gb:Congratulations, you earned %d XP!}}\n\n") % xp
        return ""
