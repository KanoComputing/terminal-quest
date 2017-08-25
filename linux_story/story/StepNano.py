import ast
import os

import time

from linux_story.PlayerLocation import generate_real_path


class StepNano:
    SAVING_NANO_PROMPT = _("Save modified buffer (ANSWERING \"No\" WILL DESTROY CHANGES) ? ")
    SAVE_FILENAME = _("File Name to Write")

    def __init__(self, client, step, location):
        self.__client = client
        self.__step = step
        self.__location = location

        self.__nano_content = ""
        self.__nano_running = False
        self.__last_nano_prompt = ""
        self.__on_filename_screen = False
        self.__nano_y = 0
        self.__save_prompt_showing = False
        self.__last_nano_filename = ""
        self.__editable = ""
        self.__goal_nano_save_name = ""
        self.__goal_nano_end_content = ""

        # set as part of the step
        self.__goal_nano_filepath = ""

        self.__last_user_input = ""

    def set_nano_running(self, nano_running):
        self.__nano_running = nano_running

    def get_nano_running(self):
        return self.__nano_running

    def set_last_nano_filename(self, filename):
        self.__last_nano_filename = filename

    def get_last_nano_filename(self):
        return self.__last_nano_filename

    def get_editable(self):
        return self.__editable

    def set_editable(self, editable):
        self.__editable = editable

    def set_nano_content(self, nano_content):
        self.__nano_content = nano_content

    def get_nano_content(self):
        return self.__nano_content

    def set_goal_nano_save_name(self, goal_nano_save_name):
        self.__goal_nano_save_name = goal_nano_save_name

    def get_goal_nano_save_name(self):
        return self.__goal_nano_save_name

    def set_on_filename_screen(self, on_filename_screen):
        self.__on_filename_screen = on_filename_screen

    def get_on_filename_screen(self):
        return self.__on_filename_screen

    def set_save_prompt_showing(self, showing):
        self.__save_prompt_showing = showing

    def get_save_prompt_showing(self):
        return self.__save_prompt_showing

    def set_goal_nano_end_content(self, goal_nano_end_content):
        self.__goal_nano_end_content = goal_nano_end_content

    def get_goal_nano_end_content(self):
        return self.__goal_nano_end_content

    def get_last_prompt(self):
        return self.__last_nano_prompt

    def set_last_prompt(self, last_prompt):
        self.__last_nano_prompt = last_prompt

    def get_goal_nano_filepath(self):
        return self.__goal_nano_filepath

    def set_goal_nano_filepath(self, goal_path):
        self.__goal_nano_filepath = goal_path

    def check_nano_content_default(self):
        if not self.get_nano_running():
            if self.get_last_nano_filename() == self.get_goal_nano_save_name():
                return True

        elif self.get_on_filename_screen() and self.get_nano_content().strip() == self.get_goal_nano_end_content():
            if self.get_editable() == self.get_goal_nano_save_name():
                hint = \
                    _("\n{{gb:Press}} {{ob:Enter}} {{gb:to confirm the filename.}}")
            else:
                hint = \
                    _("\n{{gb:Type}} {{yb:%s}} {{gb:and press}} {{yb:Enter}}") % self.get_goal_nano_save_name()
            self.send_hint(hint)
            return False

        elif self.get_on_filename_screen():
            hint = (
                _("\n{{ob:Oops, your text isn't correct. Press}} {{yb:Ctrl C}} {{ob:to cancel.}}")
            )
            self.send_hint(hint)
            return False

        elif self.get_save_prompt_showing():
            if self.get_nano_content().strip() == self.get_goal_nano_end_content():
                hint = (
                    _("\n{{gb:Press}} {{ob:Y}} {{gb:to confirm that you want to save.}}")
                )
            else:
                hint = (
                    _("\n{{rb:Your text is not correct! Press}} {{yb:N}} {{rb:to exit nano.}}")
                )
            self.send_hint(hint)
            return False

        elif self.get_nano_content().strip() == self.get_goal_nano_end_content():
            hint = \
                _("\n{{gb:Excellent, you typed}} {{yb:%s}}{{gb:. Now press}} {{yb:Ctrl X}} {{gb:to exit.}}") \
                % self.get_goal_nano_end_content()
            self.send_hint(hint)
            return False

        return False

    def check_nano_input(self):
        """This is not called anywhere by default. The intention is that is
        this is called after nano has been closed in check_command.
        """

        end_path = generate_real_path(self.get_goal_nano_filepath())

        if os.path.exists(end_path):
            f = open(end_path, "r")
            text = f.read()
            f.close()

            if text.strip() == self.get_goal_nano_end_content():
                return True
            else:
                self.send_hint(
                    _("\n{{rb:Your text is not correct! Type}} {{yb:nano %s}} {{rb:to try again.}}")
                    % self.get_goal_nano_save_name()
                )
                return False
        else:
            self.send_hint(
                _("\n{{rb:The file path}} {{lb:%s}} {{rb:does not exist - did you save your file correctly?}}")
                % end_path)
            return False

    def get_correct_nano_user_cmd(self):
        return "nano {}".format(self.get_goal_nano_save_name())

    def opened_nano(self, line):
        """This is called when user has just opened nano.
        Use to display custom message.
        Default behaviour - if there is goal end text to be written in nano,
        display a hint telling the user what to write and how to exit.
        """
        hint = None

        # TODO: fix this line. Should not compare directly to the save-anme, but instead the full path
        if not line == self.get_goal_nano_save_name():
            hint = _(
                "\n{{rb:Oops, you opened the wrong file! Press}} " +
                "{{yb:Ctrl X}} {{rb:to exit.}}"
            )

        elif self.get_goal_nano_end_content():
            hint = _(
                "\n{{gb:You've opened nano! Now make sure the file says}} " +
                "{{yb:%s}}{{gb:. If you want to exit, press}} {{yb:Ctrl X}}{{gb:.}}"
            ) % self.get_goal_nano_end_content()

        self.send_hint(hint)

    def __cancelled_save(self):
        """
        If the response of any prompt or statusbar is Cancel,
        then everything should be set to False
        """
        self.set_save_prompt_showing(False)
        self.set_on_filename_screen(False)

    def get_pipe_contents(self):
        """
        This updates information about the state of the system while nano is running.
        """
        pipe_name = "/tmp/linux-story-nano-pipe"

        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)
        f = open(pipe_name)

        while self.get_nano_running():
            time.sleep(0.2)
            line = None

            for line in iter(f.readline, ''):
                data = ast.literal_eval(line)

                if "contents" in data:
                    self.__contents_changed(data["contents"])

                if "statusbar" in data:
                    self.__status_bar_changed(data["statusbar"])

                if "response" in data:
                    self.__response_changed(data["response"])

                if "prompt" in data:
                    editable = None
                    if "editable" in data:
                        editable = data["editable"]
                    self.__prompt_changed(data["prompt"], editable)

                if "saved" in data:
                    self.set_last_nano_filename(data["filename"])

                if "finish" in data:
                    self.quit_nano()
            else:
                # TODO: this doesn't get hit if the user does a backspace
                if line:
                    self.__step.check_nano_contents()
                    if not self.get_nano_running():
                        return

    def __contents_changed(self, contents):
        # self.__cancelled_save()
        # if self.get_nano_content() != self.get_goal_nano_end_content():
        self.__set_nano_content_values(contents)

    def __prompt_changed(self, prompt, editable):
        self.set_last_prompt(prompt)
        if editable:
            self.set_editable(editable)

        if prompt == self.SAVE_FILENAME:
            self.set_save_prompt_showing(False)
            self.set_on_filename_screen(True)
        elif prompt == self.SAVING_NANO_PROMPT:
            self.set_save_prompt_showing(True)
            self.set_on_filename_screen(False)

    def __response_changed(self, value):
        if self.get_last_prompt() == self.SAVING_NANO_PROMPT:
            if value.lower() == "cancel":
                self.__cancelled_save()

            elif value.lower() == "yes":
                self.set_save_prompt_showing(True)
                self.set_on_filename_screen(True)

            elif value.lower() == "no":
                self.quit_nano()

        elif self.get_last_prompt() == self.SAVE_FILENAME:
            if value.lower() == "no":
                self.quit_nano()
            elif value.lower() == "cancel" or value.lower() == "aborted enter":
                self.__cancelled_save()

    def __status_bar_changed(self, value):
        if value.strip().lower() == "cancelled":
            self.__cancelled_save()

    def quit_nano(self):
        self.__cancelled_save()
        self.set_nano_running(False)

    def __set_nano_content_values(self, content_dict):
        nano_content = "\n".join(content_dict["text"])
        self.set_nano_content(nano_content)
        self.set_save_prompt_showing(False)

    def send_hint(self, string):
        self.__client.send_hint(string)
