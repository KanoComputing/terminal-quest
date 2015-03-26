# common.py

# This would contain all the common names across the OS

import os

# Constants

# /home/user/
HOME_FOLDER = os.path.expanduser('~')

# This is where the filetree that the user ineracts with.
TREE_HOME = os.path.join(HOME_FOLDER, '.linux-story')

# The contents of this folder are backed up online
CONTENT_FOLDER = os.path.join(HOME_FOLDER, 'Terminal-Quest-content')

# This is the yaml file that we store the state of the current file system in
# The problem with this system is we don't have the contents of the file.
# Can we save the whole file tree?  Surely that's quicker.
TREE_SNAPSHOT = os.path.join(CONTENT_FOLDER, 'tree.yml')
