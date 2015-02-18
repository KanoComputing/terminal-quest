#!/usr/bin/env python

# step_helper_functions.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Functions specific for use in Step class


def unblock_command_list(line, list_of_commands):
    line = line.strip()
    if ("mv" in line or "cd" in line) and \
            line not in list_of_commands and \
            not line.strip() == 'mv --help':

        print 'Nice try! But you do not need that command for this challenge'
        return True
