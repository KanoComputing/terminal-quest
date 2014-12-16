#!/usr/bin/env python

# helper_functions.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Helper functions.

import os
import sys
import time
import readline
import re

from kano.colours import colourize256, decorate_string


home = os.path.expanduser("~")
hidden_dir = os.path.join(home, ".linux-story")


def debugger(text):
    if False:
        print text


def get_script_cmd(string, current_dir, tree):
    is_script = False

    if string.startswith("./"):
        string = string[2:]
        real_loc = tree[current_dir].path
        script = os.path.join(real_loc, string)

    elif string.startswith("/"):
        script = string

    else:
        real_loc = tree[current_dir].path
        script = os.path.join(real_loc, string)

    # directories are executable, so exclude directories
    if os.path.exists(script) and not os.path.isdir(script):
        is_script = is_exe(script)

    return is_script, script


def is_exe(fpath):
    return os.access(fpath, os.X_OK)


# TODO: tidy up
def colour_file_dir(path, f):
    if os.path.isfile(path) and is_exe(path):
        f = colourize256(f, 118, None, True)
    elif os.path.isdir(path):
        f = "{{b" + f + "}}"
        f = parse_string(f)
    elif os.path.islink(path):
        f = decorate_string(f, "cyan", None)

    return f


def relative_loc_is_home(current_dir, tree):
    real_loc = tree[current_dir].path
    if real_loc == hidden_dir:
        return True
    return False


# This is to help the completion function in the classes
# we give this function a possible list of files and directories
# list_type = "dirs", "files", or "both"
def get_completion_desc(current_dir, tree, line, list_type="both"):

    # list of directories
    # command will be of the form:
    # "command_name" -params directory/directory/(dir OR file)
    elements = line.split(" ")

    # if the last element is a load of directories (no guarentee) then we need
    # to pick the last element to compare against
    dirs = elements[-1].split("/")
    direct_descs = tree.show_type(current_dir, list_type)
    final_list = []

    for d in dirs:
        if d in direct_descs:
            final_list.append(d)
            direct_descs = tree.show_type(d, list_type)

    # return the final element
    if final_list:
        return final_list[-1]
    return current_dir


# Colourise text
def get_preset_from_id(id):
    if id == "r":
        return 160
    elif id == "g":
        return 28
    elif id == "o":
        return 202
    elif id == "y":
        return 220
    elif id == "b":
        return 27
    elif id == "p":
        return 197
    elif id == "c":
        return 123
    elif id == "w":
        return 231
    elif id == "R":
        return 9
    elif id == "G":
        return 46
    elif id == "O":
        return 208
    elif id == "Y":
        return 226
    elif id == "B":
        return 81
    elif id == "P":
        return 205
    else:
        # lilac
        # return 147
        return 231


def message_type_preset(message_type):
    preset = {"hint": "r", "story": None, "command": None, "output": None}
    return get_preset_from_id(preset[message_type])


def parse_string(string, message_type="story", input=False):
    default_preset = message_type_preset(message_type)
    if input:
        colour_function = colourizeInput256
    else:
        colour_function = colourize256

    if string.find("{{") == -1:
        string = colour_function(string, default_preset, bold=False)
        return string

    # First part of the string
    while string.find("{{") != -1:
        pos1 = string.index("{{")
        first_part = string[:pos1]
        # Last part of the string
        pos2 = string.index("}}")
        last_part = string[pos2 + 2:]
        # Preset id
        preset_id = string[pos1 + 2]
        preset = get_preset_from_id(preset_id)
        # Colour part of the string
        colour_part = string[pos1 + 3:pos2]

        colour_part = colour_function(colour_part, preset, bold=True)
        first_part = colour_function(first_part, default_preset, bold=False)

        if string.find("{{") != -1:
            last_part = colour_function(last_part, default_preset, bold=False)

        string = first_part + colour_part + last_part

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


def typing_animation(string):
    # Get number of characters from terminal
    rows, columns = os.popen('stty size', 'r').read().split()
    columns = int(columns)
    line_width = 0

    while string:

        char = string[:1]
        e = string[:3]

        if e == "[1m":
            line_width += 1
            new_char = string[:7]
            sys.stdout.write(new_char)
            string = string[7:]
        elif e == ";5;":
            line_width += 1
            new_char = string[:7]
            sys.stdout.write(new_char)
            string = string[7:]
        elif e == "[0m":
            line_width += 1
            new_char = string[:3]
            sys.stdout.write(new_char)
            string = string[3:]
        else:
            if char == " ":
                # calculate distance to next line
                next_word = string.split(" ")[1]

                # remove all ansi escape sequences to find the real word length
                ansi_escape = re.compile(r'\x1b[^m]*m')
                clean_word = ansi_escape.sub('', next_word)
                next_word_len = len(clean_word)

                if line_width + next_word_len >= columns:
                    sys.stdout.write("\n")
                    line_width = 0
                else:
                    sys.stdout.write(" ")
                    line_width += 1
                time.sleep(0.04)

            elif char == "\n":
                sys.stdout.write(char)
                time.sleep(0.8)
                line_width = 0
            else:
                sys.stdout.write(char)
                time.sleep(0.03)
                line_width += 1
            string = string[1:]

        sys.stdout.flush()


def print_challenge_title(challenge_number):
    fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "animation/" + challenge_number
    )
    with open(fpath) as f:
        for line in f.readlines():
            print line.rstrip()
    print ""
