#!/usr/bin/env python

# paths.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import os

# setting up directories
current_dir = os.path.abspath(os.path.dirname(__file__))
prev_dir = os.path.join(current_dir, "..")

# media dir
media_local = os.path.join(prev_dir, 'media')
media_usr = '/usr/share/linux-story/media'

if os.path.exists(media_local):
    common_media_dir = media_local
elif os.path.exists(media_usr):
    common_media_dir = media_usr
else:
    raise Exception('Neither local nor usr media dir found!')

css_dir = os.path.join(current_dir, 'gtk3', 'css')
