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
    elif id == "l":
        return 147
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
        # white
        return 231


def parse_string(string, message_type="story", input=False):
    default_preset = get_preset_from_id(message_type)
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


# Try spliting the words up into an array of groups of characters,
# that all need to get printed out one at a time
def typing_animation(string):
    rows, columns = os.popen('stty size', 'r').read().split()
    letters = []
    total_width = 0

    # First, process string.  Strip each character off unless it starts with \033
    # Then, strip it off in a chunk
    while len(string) != 0:

        if string.startswith('\033'):
            index2 = string.find('m')  # First time m comes up is directly after the selected number
            substring = string[0: index2 + 1]
            string = string[index2 + 1:]
            letters.append(substring)
            total_width += 1

        # If character is " ", see if we should replace it with a newline
        elif string.startswith(' '):
            # calculate distance to next line
            next_word = string.split(" ")[1]

            # remove all ansi escape sequences to find the real word length
            ansi_escape = re.compile(r'\x1b[^m]*m')
            clean_word = ansi_escape.sub('', next_word)
            next_word_len = len(clean_word)

            if total_width + next_word_len >= int(columns):
                total_width = 0
                letters.append('\n')
            else:
                total_width += 1
                letters.append(" ")
            string = string[1:]

        else:
            letters.append(string[0])
            string = string[1:]
            total_width += 1

    for l in letters:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(0.1)


def print_challenge_title(challenge_number="1"):
    fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "animation/" + challenge_number
    )
    with open(fpath) as f:
        for line in f.readlines():
            print line.rstrip()
    print ""
