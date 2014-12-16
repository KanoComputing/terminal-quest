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
from linux_story.paths import common_media_dir


class Spellbook(Gtk.EventBox):

    SPELLBOOK_BORDER = 1
    SPELL_BORDER = 1
    CMD_HEIGHT = 80
    CMD_WIDTH = 80
    HEIGHT = 100

    def __init__(self):
        self.stop = False

        # TODO: fix this, is hacky.
        # First time we launch the spellbook, we want to hide it
        self.first = True

        Gtk.EventBox.__init__(self)

        background = Gtk.EventBox()
        background.get_style_context().add_class("spellbook_background")

        self.grid = Gtk.Grid()
        self.add(background)
        background.add(self.grid)

        screen = Gdk.Screen.get_default()
        self.win_width = screen.get_width()
        self.win_height = screen.get_height()

        self.WIDTH = self.win_width / 2

        self.set_size_request(self.WIDTH, self.HEIGHT)

        self.pack_locked_spells()

    def create_spell(self, name, locked=False):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_size_request(self.CMD_WIDTH, self.CMD_HEIGHT)
        box.set_margin_top(10)
        box.set_margin_left(10)
        box.set_margin_right(10)
        box.set_margin_bottom(10)

        icon_background = Gtk.EventBox()
        icon_background.get_style_context().add_class("spell_icon_background")
        box.pack_start(icon_background, False, False, 0)

        label_background = Gtk.EventBox()
        label_background.get_style_context().add_class("spell_label_background")

        if locked:
            filename = os.path.join(common_media_dir, "padlock.png")
            icon_background.get_style_context().add_class("locked")
            label_background.get_style_context().add_class("locked")

        else:
            filename = os.path.join(common_media_dir, name + ".png")

        icon = Gtk.Image.new_from_file(filename)
        icon_background.add(icon)

        box.pack_start(label_background, False, False, 0)

        label = Gtk.Label(name)
        label.get_style_context().add_class("spell_command")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label_background.add(label)

        return box

    def pack_spells(self, commands):
        left = 0

        if commands:
            for command in commands:
                if (left + 1) * (self.CMD_WIDTH + 20) < self.win_width:
                    box = self.create_spell(command)
                    child = self.grid.get_child_at(left, 0)
                    self.grid.remove(child)
                    self.grid.attach(box, left, 0, 1, 1)
                    left += 1

    def pack_locked_spells(self):
        left = 0

        while (left + 1) * (self.CMD_WIDTH + 20) < self.win_width:
            locked_box = self.create_spell("...", locked=True)
            self.grid.attach(locked_box, left, 0, 1, 1)
            left += 1

    def repack_spells(self, commands):
        self.pack_spells(commands)
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

        #delete_file("hide-spellbook")

    def get_command_list(self):
        if file_exists("commands"):
            command_string = read_file("commands")
            command_list = command_string.split(" ")
            return command_list

    def check_files(self):
        while not self.stop:
            if file_exists("commands"):
                commands = self.get_command_list()
                GObject.idle_add(self.repack_spells, commands)
                self.delete_file()
            if file_exists("exit"):
                Gtk.main_quit()
                sys.exit(0)
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
