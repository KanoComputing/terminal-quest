#!/usr/bin/env python

from gi.repository import Vte
from gi.repository import GLib
import os


class Terminal_Ui(Vte.Terminal):
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
        self.set_scrollback_lines(0)

    def launch_command(self, command):
        command = "temp=$(tty) ; " + command + " > $temp | clear\n"
        length = len(command)
        self.feed_child(command, length)
