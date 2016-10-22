# common.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# This contains all the common names across the OS.


import os
import json

# setting up directories
current_dir = os.path.abspath(os.path.dirname(__file__))

# media dir
media_local = os.path.join(current_dir, '../media')
media_usr = '/usr/share/linux-story/media'

if os.path.exists(media_local):
    common_media_dir = media_local
elif os.path.exists(media_usr):
    common_media_dir = media_usr
else:
    raise Exception('Neither local nor usr media dir found!')

css_dir = os.path.join(current_dir, 'gtk3', 'css')

ascii_assets_dir = os.path.join(current_dir, 'ascii_assets')
localized_story_files_dir_pattern = os.path.join(ascii_assets_dir, 'locale', '{}', 'story_files')
fallback_story_files_dir = os.path.join(ascii_assets_dir, 'story_files')
sounds_dir = os.path.join(common_media_dir, 'sounds')
images_dir = os.path.join(common_media_dir, 'images')

# Constants

# /home/user/
home_folder = os.path.expanduser('~')

# This is where the filetree that the user interacts with.
tq_file_system = os.path.join(home_folder, '.linux-story')

# The contents of this folder are backed up online
tq_backup_folder = os.path.join(home_folder, 'Terminal-Quest-content')


def get_max_challenge_number():
    '''
    Returns:
        str: string of the maximum challenge number as saved in
            kano-profile.
    '''

    # Hardcoded path, perhapes change it later
    path = "/usr/share/kano-profile/rules/app_profiles.json"
    f = open(path)
    str_data = f.read()
    f.close()

    dict_data = json.loads(str_data)
    max_level = dict_data['linux-story']['max-level']

    return max_level


def get_username():
    return os.environ["LOGNAME"]
