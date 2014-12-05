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

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.file_functions import read_file, file_exists, delete_file
from kano.gtk3.apply_styles import apply_styling_to_screen


class Spellbook(Gtk.EventBox):
    CMD_WIDTH = 80
    CMD_HEIGHT = 80
    CSS_FILE = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "css/spellbook.css"
    )
    SPELLBOOK_BORDER = 1
    SPELL_BORDER = 1

    def __init__(self):
        apply_styling_to_screen(self.CSS_FILE)
        self.stop = False

        Gtk.EventBox.__init__(self)
        self.get_style_context().add_class("spellbook_border")

        background = Gtk.EventBox()
        background.get_style_context().add_class("spellbook_background")
        background.set_margin_right(self.SPELLBOOK_BORDER)
        background.set_margin_left(self.SPELLBOOK_BORDER)
        background.set_margin_top(self.SPELLBOOK_BORDER)
        background.set_margin_bottom(self.SPELLBOOK_BORDER)

        self.grid = Gtk.Grid()
        self.add(background)
        background.add(self.grid)

        screen = Gdk.Screen.get_default()
        self.win_width = screen.get_width()
        self.win_height = screen.get_height()

        self.width = self.win_width / 2
        self.height = 200

        self.set_size_request(self.width, self.height)

    def create_command(self, name):
        box = Gtk.Box()
        label = Gtk.Label(name)
        label.get_style_context().add_class("spell_label")
        box.add(label)

        align = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
        align.add(box)

        background = Gtk.EventBox()
        background.add(align)
        background.get_style_context().add_class("spell_background")
        background.set_margin_right(self.SPELL_BORDER)
        background.set_margin_bottom(self.SPELL_BORDER)

        border = Gtk.EventBox()
        border.get_style_context().add_class("spell_border")
        border.set_size_request(self.CMD_WIDTH, self.CMD_HEIGHT)
        border.add(background)

        return border

    def pack_commands(self):
        # these are counters monitoring where the command is placed on the
        # window
        top = 0
        left = -1
        total_width = 0
        total_height = 0

        commands = self.get_command_list()

        if commands:
            for command in commands:
                total_width += self.CMD_WIDTH
                total_height += self.CMD_HEIGHT

                if total_width > self.width:
                    top += 1
                else:
                    left += 1

                box = self.create_command(command)
                self.grid.attach(box, left, top, 1, 1)

        self.show_all()

    def unpack_commands(self):
        for child in self.grid:
            self.grid.remove(child)

    def repack_commands(self):
        self.unpack_commands()
        self.pack_commands()

    def get_command_list(self):
        if file_exists("commands"):
            command_string = read_file("commands")
            command_list = command_string.split(" ")
            return command_list

    def check_files(self):
        while not self.stop:
            if file_exists("commands"):
                GObject.idle_add(self.repack_commands)
                self.delete_file()

    def delete_file(self):
        delete_file("commands")


class SpellbookThread(threading.Thread):
    def __init__(self, spellbook):
        threading.Thread.__init__(self)
        self.__stop = False
        self.spellbook = spellbook

    def stop(self):
        self.spellbook.delete_file()
        self.__stop = True

    def run(self):
        self.spellbook.check_files()
