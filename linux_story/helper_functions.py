#!/usr/bin/env python

# helper_functions.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Helper functions used across the system.

import os
import subprocess

from kano.colours import colourize256, decorate_string
from kano_profile.apps import (
    save_app_state_variable, load_app_state_variable,
    increment_app_state_variable
)
from linux_story.common import common_media_dir


def debugger(text):
    '''Change first line to "if True:" to show all the debugging lines
    '''

    if False:
        print text


def get_script_cmd(string, real_path):
    '''Checks whether the string (from the user's point of view)
    is an executible.
    So we convert the path entered into the real path (i.e. including the
    .linux-story) and check it's a file and and executable
    '''

    is_script = False

    if string.startswith("./"):
        string = string[2:]
        script = os.path.join(real_path, string)

    elif string.startswith("/"):
        script = string

    else:
        script = os.path.join(real_path, string)

    # directories are executable, so exclude directories
    if os.path.exists(script) and not os.path.isdir(script):
        is_script = is_exe(script)

    return is_script, script


def is_exe(fpath):
    return (os.path.isfile(fpath) and os.access(fpath, os.X_OK))


# TODO: tidy up
def colour_file_dir(path, f):
    '''Colourize the files and directories shown by ls
    '''

    if os.path.isfile(path) and is_exe(path):
        f = colourize256(f, 118, None, True)
    elif os.path.isdir(path):
        f = "{{b" + f + "}}"
        f = parse_string(f)
    elif os.path.islink(path):
        f = decorate_string(f, "cyan", None)

    return f


def play_sound(object_name):
    '''object is the string representing the object
    the options are 'alarm' and 'bell'
    '''

    sound_path = os.path.join(
        common_media_dir,
        "sounds",
        object_name + '.wav'
    )

    subprocess.Popen(
        ["/usr/bin/aplay", sound_path],
        stderr=subprocess.STDOUT, stdout=subprocess.PIPE
    )


def get_preset_from_id(id):
    '''Translate the letter IDs into the colour codes
    r=red, g=green, y=yellow, b=blue, p=pink, c=cyan, w=white, l=lilac
    The capital letters are different shades of the same colour
    '''

    if id == "r":
        return 160
    elif id == "g":
        return 28
    elif id == "o":
        return 202
    elif id == "y":
        return 220
    elif id == "b":
        return 69
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
    '''Change a string of the form "{{bhello}}" to a the string "hello"
    that appears blue in a terminal
    '''

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


def print_gained_exp(challenge, fork):
    old_xp = load_app_state_variable('linux_story', challenge + '_' + fork)
    # Look up XP here
    new_xp = 0
    xp_gained = new_xp - old_xp
    if xp_gained > 0:
        return "Fantastic! You gained {} experience points!".format(xp_gained)
    else:
        return None


def record_user_interaction(instance, base_name):
    '''This is to store commands the user does.

    instance: the class instance.
    base_name: a string for the identity of the command.
    '''

    class_instance = instance.__class__.__name__
    challenge_number = instance.challenge_number
    profile_var_name = "{} {} {}".format(
        base_name, challenge_number, class_instance
    )

    # First, try loading the profile variable name
    # If the value is None, then make it True and increment the total.
    already_done = load_app_state_variable("linux-story", profile_var_name)

    # If the command has not been done yet in this class, then increment the
    # total
    if not already_done:
        save_app_state_variable("linux-story", profile_var_name, True)
        total_name = "{} total".format(base_name)
        increment_app_state_variable("linux-story", total_name, 1)

        # If total reaches a certain amount, then can award XP.
