#!/usr/bin/env python

# linux-story-gui
#
# Copyright (C) 2014 Kano Computing Ltd
# License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
#
# Author: Caroline Clark <caroline@kano.me>
# Launches linux tutorial in a Gtk application

import os
import sys
from gi.repository import Gtk, Gdk, GObject
import threading
import time

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.file_functions import read_file, file_exists, delete_file, delete_dir
from kano.gtk3.apply_styles import apply_styling_to_screen
from kano.utils import get_user


class Spellbook(Gtk.EventBox):
    CSS_FILE = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "css/spellbook.css"
    )
    SPELLBOOK_BORDER = 1
    SPELL_BORDER = 1
    DESCRIPTIONS = {
        "ls": "Take a look around you",
        "cd": "Go somewhere new",
        "cat": "Print the contents of a file",
        "title": "{}'s spellbook".format(get_user())
    }

    def __init__(self):
        apply_styling_to_screen(self.CSS_FILE)
        self.stop = False
        # TODO: fix this, is hacky.  First time we launch the spellbook, we want to hide it
        self.first = True

        Gtk.EventBox.__init__(self)
        self.get_style_context().add_class("spellbook_border")

        background = Gtk.EventBox()
        background.get_style_context().add_class("spellbook_background")

        self.grid = Gtk.Grid()
        self.add(background)
        background.add(self.grid)

        screen = Gdk.Screen.get_default()
        self.win_width = screen.get_width()
        self.win_height = screen.get_height()

        self.width = self.win_width / 2
        self.height = 200

        self.set_size_request(self.width, self.height)

    def create_command(self, name, top):

        CMD_HEIGHT = 50
        CMD_WIDTH = self.width

        box = Gtk.Box()
        box.set_size_request(CMD_WIDTH, CMD_HEIGHT)

        label_background = Gtk.EventBox()
        label_background.set_size_request(50, 50)
        description_background = Gtk.EventBox()
        description_background.set_size_request(self.width - 50, 50)

        if name == "title":
            label_background.get_style_context().add_class("light_yellow_grey")
            description_background.get_style_context().add_class("dark_yellow_grey")
            # add icon
        else:
            label = Gtk.Label(name)
            label.get_style_context().add_class("spell_command")
            label_background.add(label)
            if top % 2 == 1:
                label_background.get_style_context().add_class("dark_blue")
                description_background.get_style_context().add_class("dark_grey")
            else:
                label_background.get_style_context().add_class("light_blue")
                description_background.get_style_context().add_class("light_grey")

        description = Gtk.Label(self.DESCRIPTIONS[name])
        description.get_style_context().add_class("spell_description")
        description.set_alignment(0, 0.5)
        description.set_padding(10, 0)
        description_background.add(description)

        box.pack_start(label_background, False, False, 0)
        box.pack_start(description_background, False, False, 0)

        return box

    def pack_commands(self, commands):
        top = 0

        if commands:
            for command in commands:
                box = self.create_command(command, top)
                self.grid.attach(box, 0, top, 1, 1)
                top += 1

    def unpack_commands(self):
        for child in self.grid:
            self.grid.remove(child)

    def repack_commands(self, commands):
        self.unpack_commands()
        commands = ["title"] + commands
        self.pack_commands(commands)
        if self.first:
            self.first = False
        else:
            self.show_all()

    # TODO: use this to hide UI?
    def hide_ui(self):

        win = self.get_toplevel()
        win.show_all()
        win.terminal.hide()
        win.spellbook.hide()

        time.sleep(5)

        win.show_all()
        win.spellbook.show_all()
        win.terminal.show_all()

        delete_file("hide-spellbook")

    def get_command_list(self):
        if file_exists("commands"):
            command_string = read_file("commands")
            command_list = command_string.split(" ")
            return command_list

    def check_files(self):
        while not self.stop:
            if file_exists("commands"):
                commands = self.get_command_list()
                GObject.idle_add(self.repack_commands, commands)
                self.delete_file()
            #if file_exists("hide-spellbook"):
            #    GObject.idle_add(self.hide_ui)
            #else:
            #    GObject.idle_add(self.show_all)

    def delete_file(self):
        if file_exists("commands"):
            delete_file("commands")


class SpellbookThread(threading.Thread):
    def __init__(self, spellbook):
        threading.Thread.__init__(self)
        self.spellbook = spellbook

    def run(self):
        self.spellbook.check_files()
        delete_dir()
