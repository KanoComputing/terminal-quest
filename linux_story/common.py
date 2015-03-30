# common.py

# This would contain all the common names across the OS

import os

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

# Constants

# /home/user/
home_folder = os.path.expanduser('~')

# This is where the filetree that the user interacts with.
tq_file_system = os.path.join(home_folder, '.linux-story')

# The contents of this folder are backed up online
tq_backup_folder = os.path.join(home_folder, 'Terminal-Quest-content')

# This is the yaml file that we store the state of the current file system in
# The problem with this system is we don't have the contents of the file.
# Can we save the whole file tree?  Surely that's quicker.
tq_backup_tree = os.path.join(tq_backup_folder, 'tree.yml')
