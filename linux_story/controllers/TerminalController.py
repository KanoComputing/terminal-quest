import os
import sys
import pygame
from pygame.locals import *
import string

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.models.models import TerminalAll
from linux_story.models.filesystem import (
    make_filesystem_from_config, remove_file_system
)
from linux_story.view.TerminalWindow import TerminalWindow


class TerminalController():
    def __init__(self, model):
        self._running = True
        self._view = TerminalWindow()
        self._model = model

    def _set_view_prompt(self, location):
        self._view.set_prompt(location)

    def update_view_prompt(self):
        self._set_view_prompt(self._model.position)

    def get_view_input(self):
        return self._view.input()

    def give_model_input(self, input):
        if input == "exit":
            self._running_commands = False
            return

        output = self._model.receive_command(input)
        if output:
            if type(output) == str:
                self._view.write_text(output + "\n")
            elif type(output) == list:
                output = " ".join(output) + "\n"
                self._view.write_text(output)

        # Update prompt with new info
        self.update_view_prompt()

    def start(self):
        self.update_view_prompt()
        tab_pressed = 0
        text = ""
        (cursorx, cursory) = self._view.cursor

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)

                    if key == "backspace":
                        text = text[:-1]
                        tab_pressed = 0
                    elif key == "tab":
                        tab_pressed += 1
                        autocomplete = self._model.autocomplete(text)
                        text += "\n"
                        self._view.set_cursor(cursorx, cursory)
                        self._view.write_text(text + " ")
                        self._view.write_text(autocomplete)
                        self.update_view_prompt()
                        text = ""
                        # Run the right autocomplete command.
                    elif key == "return":
                        cursory += 1
                        self._view.set_cursor(0, cursory)
                        self.give_model_input(text)
                        (cursorx, cursory) = self._view.cursor
                        text = ""
                        tab_pressed = 0
                    else:
                        text += event.unicode
                        tab_pressed = 0
                        print "{} pressed".format(key)

                    print "text = {}".format(text)
                    # This forces the cursor to where it was, so undoes the automatic
                    # work.
                    # Might want to revert this
                    self._view.set_cursor(cursorx, cursory)
                    self._view.write_text(text + " ")


if __name__ == "__main__":
    remove_file_system()
    filesystem = [
        {
            "name": "~",
            "type": "directory",
            "children": [
                {
                    "name": "parent_directory",
                    "type": "directory",
                    "children": [
                        {
                            "name": "file1",
                            "type": "file"
                        },
                        {
                            "name": "file2",
                            "type": "file"
                        },
                        {
                            "name": "file3",
                            "type": "file"
                        },
                        {
                            "name": "dir1",
                            "type": "directory"
                        },
                        {
                            "name": "dir2",
                            "type": "directory"
                        },
                        {
                            "name": "dir3",
                            "type": "directory"
                        }
                    ]
                }
            ]
        }
    ]
    make_filesystem_from_config(filesystem)
    terminal = TerminalAll("~")
    tc = TerminalController(terminal)
    tc.start()
