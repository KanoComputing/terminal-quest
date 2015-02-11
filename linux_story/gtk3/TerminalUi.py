#!/usr/bin/env python

# TerminalUi.py
#
# Copyright (C) 2014 Kano Computing Ltd
# License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
#
# Author: Caroline Clark <caroline@kano.me>
# Terminal Gtk emulator


from gi.repository import Vte
from gi.repository import GLib, GObject
import os


class TerminalUi(Vte.Terminal):
    def __init__(self):
        Vte.Terminal.__init__(self)
        self.fork_command_full(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/sh"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None)

        # This prevents the user scrolling back through the history
        # self.set_scrollback_lines(0)

    def launch_command(self, command):
        command = "temp=$(tty) ; " + command + " > $temp | clear\n"
        length = len(command)
        self.feed_child(command, length)


class MyObject(GObject.GObject):
    __gsignals__ = {
        'my_signal': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def do_my_signal(self):
        print "class method for `my_signal' called with argument"
