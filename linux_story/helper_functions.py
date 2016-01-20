# helper_functions.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Helper functions used across the system.


import os
import subprocess

from kano.colours import colourize256, decorate_string
from kano_profile.apps import \
    save_app_state_variable, load_app_state_variable, \
    increment_app_state_variable
from kano.logging import logger

from linux_story.common import common_media_dir, story_files_dir


def debugger(text):
    '''
    Change first line to "if True:" to show all the debugging lines.
    '''

    if False:
        print text


def get_script_cmd(string, real_path):
    '''
    Checks whether the path (from the user's point of view)
    is an executable.

    We convert the path entered into the real path (i.e. including the
    .linux-story) and check it's a file and and executable.

    Args:
        string (str): command that the user has typed.
        real_path (str): the path that the user is currently based at.

    Returns:
        tuple = (bool, str):
            The first argument says if the script is a valid executable.
            The second argument gives the full filepath of the executable.
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


def colour_file_dir(path, f):
    '''
    Colourize the files and directories consistently

    Args:
        path (str): the full file path of the file
        f (str): the name of the filename

    Returns:
        str: the filename with the appropriate appended substrings to
            make it appear the correct colour in a terminal.
    '''

    if os.path.isfile(path) and is_exe(path):
        f = colour_string_with_preset(f, "green", False)

    elif os.path.isdir(path):
        f = colour_string_with_preset(f, "blue", False)

    elif os.path.islink(path):
        f = decorate_string(f, "cyan", None)

    return f


def play_sound(object_name):
    '''
    Args:
        object_name (str): 'alarm' or 'bell'
    Returns:
        None
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


def colour_string_with_preset(string, colour_name="white", input_fn=True):
    '''
    Args:
        string (str): the string we want to colourise.
        colour_name (str): takes the values "yellow", "white", "blue", "green"
        input_fn (bool): determines which colourise function we use.

    Returns:
        str: string which will appear with specified colour in a terminal.
    '''

    colours = {
        "yellow": 226,
        "white": 231,
        "blue": 69,
        "green": 118
    }
    if input_fn:
        colour_fn = colourize_input256
    else:
        colour_fn = colourize256

    colour_id = colours[colour_name]
    bold = True

    # For now, if colour is white, don't make it bold.
    if colour_name == "white":
        bold = False

    return colour_fn(string, colour_id, None, bold)


def colourize_input256(string, fg_num=None, bg_num=None, bold=False):
    """
    Paint the text with foreground/background colours using the
    newer 256 colour model.

    This is similar to colourize256, but it adds extra hidden characters to
    each side of the strings due to a problem with weird characters appearing
    in the terminal.
    These extra characters need to be combined with importing the readline
    library.

    Args:
        string (str): the string we want to colourize
        fg_num (int): the foreground colour
        bg_num (int): the background colour
        bold (bool): should the text be shown as bold

    Returns:
        str
    """

    if fg_num is not None:
        string = "\001\033[38;5;%dm\002%s\001\033[0m\002" % (fg_num, string)

    if bg_num is not None:
        string = "\001\033[48;5;%dm\002%s\001\033[0m\002" % (bg_num, string)

    if bold:
        string = "\001\033[1m\002%s\001\033[0m\002" % string

    return string


def record_user_interaction(instance, base_name):
    '''
    This is to store some of the user actions, so we can determine
    if the user does the optional side quests.

    Args:
        The class instance.
        base_name (str): a string for the identity of the command.
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


def get_ascii_art(name):
    """
    Load and ASCII art file.

    Args:
        name (str) - the name of the asset file

    Returns:
        ascii_art (str) - the ASCII art asset as a block of text
    """

    ascii_art = name
    asset_path = os.path.join(story_files_dir, name)

    try:
        with open(asset_path) as f:
            ascii_art = f.read()

    except (IOError, OSError) as e:
            logger.error('Could not load file {} - [{}]'.format(asset_path, e))
    except Exception as e:
            logger.warn('Unexpected error while loading the ascii art'
                        ' - [{}]'.format(e))

    return ascii_art
