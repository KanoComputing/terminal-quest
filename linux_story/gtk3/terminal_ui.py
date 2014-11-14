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
