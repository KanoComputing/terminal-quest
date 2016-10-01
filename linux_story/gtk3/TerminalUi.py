# TerminalUi.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Terminal Gtk emulator


import os

from gi.repository import Vte, GLib, Gdk, Pango


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
            None
        )

        # This prevents the user scrolling back through the history
        # self.set_scrollback_lines(0)

        # OK. So, this is "required" as a quick fix to a bug where the terminal
        # would wrap the line on itself. It is due to the MenuScreen and how the
        # main window add/removes it. By setting the column and row count to large
        # initial values, it will force to resize from large to smaller values as
        # opposed from a default 80, 24.
        self.set_size(1000, 1000)  # TODO: please fix this
        self.__setup_appearance()

    def __setup_appearance(self):
        fg_color = Gdk.Color.parse("#ffffff")[1]
        bg_color = Gdk.Color.parse("#262626")[1]
        self.set_colors(fg_color, bg_color, [])
        self.set_margin_top(10)
        self.set_margin_left(10)
        self.set_margin_right(10)
        font_desc = Pango.FontDescription()
        font_desc.set_family("monospace")
        font_desc.set_size(13 * Pango.SCALE)
        self.set_font(font_desc)

    def feed_child(self, command):
        Vte.Terminal.feed_child(self, command, len(command))

    def launch_command(self, command):
        command = "temp=$(tty) ; " + command + " > $temp | reset\n"
        self.feed_child(command)
