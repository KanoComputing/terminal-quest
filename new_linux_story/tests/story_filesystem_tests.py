#!/usr/bin/env python

# story_filesystem_tests.py
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Tests to check the filesystems made for the challenges.

import unittest
import os
import sys
import json

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from new_linux_story.common import story_data
from new_linux_story.models.filesystem import FileSystem


class SingleFileChecks(unittest.TestCase):
    def test_challenge_1_files(self):
        config_string = open(story_data, "r").read()
        config = json.loads(config_string)
        filesystem = FileSystem(config)
        (exists, f) = filesystem.path_exists("~/my-house")
        self.assertEquals(exists, True)


if __name__ == "__main__":
    unittest.main()
