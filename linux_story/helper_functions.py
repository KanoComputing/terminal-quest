# helper_functions.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Helper functions used across the system.


import os
import os.path
import gettext

from kano.colours import colourize256, decorate_string
from kano.logging import logger
from kano_profile.apps import \
    save_app_state_variable, load_app_state_variable, \
    increment_app_state_variable

from linux_story.common import \
    localized_story_files_dir_pattern, \
    fallback_story_files_dir


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
    Load an ASCII art file.

    Args:
        name (str) - the name of the asset file

    Returns:
        ascii_art (str) - the ASCII art asset as a block of text
    """

    ascii_art = name
    asset_path = get_path_to_file_in_system(name)

    try:
        with open(asset_path) as f:
            ascii_art = f.read()

    except (IOError, OSError) as e:
            logger.error('Could not load file {} - [{}]'.format(asset_path, e))
    except Exception as e:
            logger.error('Unexpected error while loading the ascii art'
                         ' - [{}]'.format(e))

    return ascii_art


def get_path_to_file_in_system(name):
    """
    Finds the path of a file (asset), first looking for any translation,
    and falling back to the default location.

    Args:
        name (str) - the name of the asset file

    Returns:
        path (str) - the path to the file (asset)
    """

    path_in_system = None

    lang_dirs = get_language_dirs()

    for lang_dir in lang_dirs:
        asset_path = os.path.join(localized_story_files_dir_pattern.format(lang_dir), name)
        if os.path.isfile(asset_path):
            path_in_system = asset_path
            break

    if path_in_system is None:
        path_in_system = os.path.join(fallback_story_files_dir, name)

    return path_in_system


language_dirs = None

def get_language_dirs():
    """
    Get possible language directories to be searched for, based on 
    the environment variables: LANGUAGE, LC_ALL, LC_MESSAGES and LANG.
    The result is memoized for future use.

    This function is inspired by python gettext.py.

    Returns:
        dirs (array) - an array of language directories
    """

    global language_dirs
    if language_dirs is not None:
        return language_dirs

    languages = []
    for envar in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
        val = os.environ.get(envar)
        if val:
            languages = val.split(':')
            break
    if 'C' in languages:
        languages.remove('C')

    # now normalize and expand the languages
    nelangs = []
    for lang in languages:
        for nelang in gettext._expand_lang(lang):
            if nelang not in nelangs:
                nelangs.append(nelang)

    language_dirs = nelangs
    return language_dirs


