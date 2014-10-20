"""
Terminal colouring functions

Copyright 2013 Red Hat, Inc.
Licensed under the GNU General Public License, version 2 as
published by the Free Software Foundation; see COPYING for details.

Taken from the LNST project: https://github.com/jpirko/lnst/
"""

__author__ = """
rpazdera@redhat.com (Radek Pazdera)
"""

import re
import sys
import readline

COLOURS = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 25,
    "cyan": 36,
    "light-gray": 37,
    "dark-gray": 90,
    "light-red": 91,
    "light-green": 92,
    "light-yellow": 93,
    "light-blue": 94,
    "light-magenta": 95,
    "light-cyan": 96,
    "white": 97,
}

PRESETS = {
    "code":           ["green", "dark-gray", True],
    "key":            ["red", "dark-gray", True],

    "faded":          ["yellow", None, False],
    "alert":          ["red", None, True],
    "highlight":      ["blue", None, True],

    "pass":           ["green", None, True],
    "fail":           ["red", None, True],

    "info":           ["green", None, True],
    "debug":          ["blue", None, True],
    "warning":        ["yellow", None, True],
    "error":          ["red", None, True],
    "none":           [None, None, False],

    # Used in colours-cli
    "command_prompt": ["light-cyan", None, False],
    "keyboard":       ["white", "light-red", True],
    "instructions":   ["light-cyan", "dark-gray", False],
    "success_text":   ["light-green", None, False],
    "success_icon":   ["white", "green", True],
    "hint_text":      ["light-yellow", None, False],
    "hint_icon":      ["dark-gray", "light-yellow", True],
    "error_text":     ["light-red", None, False],
    "error_icon":     ["white", "red", True]
}

enabled = True


def enable():
    global enabled
    enabled = True


def disable():
    global enabled
    enabled = False


def name_to_fg_colour(name):
    """ Convert name to foreground colour code.
        Returns None if the colour name isn't supported. """

    if not COLOURS.has_key(name):
        return None

    return COLOURS[name]


def name_to_bg_colour(name):
    """ Convert name to background color code.
        Returns None if the colour name isn't supported. """

    if not COLOURS.has_key(name):
        return None

    return COLOURS[name] + 10


def colourize16(string, fg_num=None, bg_num=None, bold=False):
    """ Paint the text with foreground/background colours using the
        old 16 colour model. """

    if fg_num is not None:
        string = "\033[%dm%s\033[0m" % (fg_num, string)

    if bg_num is not None:
        string = "\033[%dm%s\033[0m" % (bg_num, string)

    if bold:
        string = "\033[1m%s\033[0m" % string

    return string


def colourize256(string, fg_num=None, bg_num=None, bold=False):
    """ Paint the text with foreground/background colours using the
        newer 256 colour model. """

    if fg_num is not None:
        string = "\033[38;5;%dm%s\033[0m" % (fg_num, string)

    if bg_num is not None:
        string = "\033[48;5;%dm%s\033[0m" % (bg_num, string)

    if bold:
        string = "\033[1m%s\033[0m" % string

    return string


def colourizeInput256(string, fg_num=None, bg_num=None, bold=False):
    """ Paint the text with foreground/background colours using the
        newer 256 colour model. """

    if fg_num is not None:
        string = "\001\033[38;5;%dm\002%s\001\033[0m\002" % (fg_num, string)

    if bg_num is not None:
        string = "\001\033[48;5;%dm\002%s\001\033[0m\002" % (bg_num, string)

    if bold:
        string = "\001\033[1m\002%s\001\033[0m\002" % string

    return string


def decorate_string_only_terminal(string, fg_colour=None, bg_colour=None, bold=False):
    """ Return unmodified string if not called from terminal """

    if not sys.stdout.isatty() or not enabled:
        return string

    return decorate_string(string, fg_colour, bg_colour, bold)


def decorate_string(string, fg_colour=None, bg_colour=None, bold=False):
    """ Decorate a string using colours specified as strings. You can
        pick one from the set of 16 predefined colours from the COLOURS
        dictionary or alternatively, you can use an extended colour
        from the 256-colour palette using the "extended(colour_number)"
        syntax. To retain the default colour, use the keyword "default".

        A few examples:

            decorate_string(s, "light-blue", "extended(242)")
            decorate_string(s, "red", None, True)
            decorate_string(s, "red", None, False)
            decorate_string(s, "red", "light-gray")
    """

    extended_re = "^extended\(([0-9]+)\)$"

    # parameters for the colouring functions (fg_num, bg_num)
    # the bold flag is handled separately
    params16 = []
    params256 = []

    # This part of the code would have to be done for both fg and bg
    # We use a for loop here to avoid code duplication
    fg = True
    for colour_def in [fg_colour, bg_colour]:
        if colour_def is not None:
            # Extended definition
            match = re.match(extended_re, colour_def)
            if match:
                colour_num = int(match.group(1))
                if colour_num >= 1 and colour_num <= 255:
                    params16.append(None)
                    params256.append(colour_num)
                else:
                    msg = "Extended colour '%d' out of range (0~255)"\
                          % colour_num
                    raise Exception(msg)
            else:
                # Standard definition
                if colour_def in COLOURS.keys():
                    if fg:
                        colour = name_to_fg_colour(colour_def)
                    else:
                        colour = name_to_bg_colour(colour_def)
                    params16.append(colour)
                    params256.append(None)
                else:
                    raise Exception("Colour '%s' not supported" % fg_colour)
        else:
            params16.append(None)
            params256.append(None)
        fg = False

    string = colourize16(string, params16[0], params16[1], bold)
    string = colourize256(string, params256[0], params256[1])
    return string


def decorate_with_preset(string, preset, only_terminal=False):
    """ Decorate a string using a specified colour preset. """

    p = PRESETS[preset]

    if not only_terminal:
        return decorate_string(string, p[0], p[1], p[2])

    return decorate_string_only_terminal(string, p[0], p[1], p[2])
