#!/usr/bin/env python

# linux-story-gui
#
# Copyright (C) 2014 Kano Computing Ltd
# License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
#
# Author: Caroline Clark <caroline@kano.me>
# Launches linux tutorial in a Gtk application


from gi.repository import Gtk


class Spellbook(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.pack_commands()
        # Find unlocked commands and then pack them

    def create_command(self, name):
        box = Gtk.Box()
        label = Gtk.Label(name)
        box.add(label)

        background = Gtk.EventBox()
        background.add(box)
        return background

    def pack_commands(self):
        print "packing commands"
        top = 0
        #commands = self.get_command_list()
        commands = ["ls", "cd", "cat"]
        for command in commands:
            box = self.create_command(command)
            self.attach(box, 0, top, 1, 1)
            top = top + 1
