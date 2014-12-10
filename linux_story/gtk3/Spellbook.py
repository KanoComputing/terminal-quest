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
        self.height = 60

        self.set_size_request(self.width, self.height)

    def create_command(self, name, left):

        CMD_HEIGHT = 60
        CMD_WIDTH = 60

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_size_request(CMD_WIDTH, CMD_HEIGHT)

        background = Gtk.EventBox()
        background.set_size_request(CMD_HEIGHT, CMD_WIDTH)
        background.add(box)

        if name == "title":
            background.get_style_context().add_class("light_yellow_grey")
            # add icon
        else:
            label = Gtk.Label(name)
            label.get_style_context().add_class("spell_command")
            label.set_alignment(xalign=0.5, yalign=0.5)
            box.pack_start(label, True, False, 0)
            if left % 2 == 1:
                background.get_style_context().add_class("dark_blue")
            else:
                background.get_style_context().add_class("light_blue")

        return background

    def pack_commands(self, commands):
        left = 0

        if commands:
            for command in commands:
                box = self.create_command(command, left)
                self.grid.attach(box, left, 0, 1, 1)
                left += 1

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
