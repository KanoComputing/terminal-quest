#!/usr/bin/env python

# step_helper_functions.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Functions specific for use in Step class


def unblock_commands(line, list_of_commands):
    '''Blocks the command that start with cd and mv unless the command is in
    list_of_commands
    '''

    line = line.strip()
    if ("mv" in line or "cd" in line) and \
            line not in list_of_commands and \
            not line.strip() == 'mv --help':

        print 'Nice try! But you do not need that command for this challenge'
        return True


def unblock_commands_with_cd_hint(line, list_of_commands):
    '''Unblocks the commands and informs the user
    '''
    line = line.strip()
    if ("cd" in line and line not in list_of_commands):
        print "You're close, but you entered an unexpected destination path. Try going somewhere else."
        return True

    elif ("mv" in line) and \
            not line.strip() == 'mv --help':

        print 'Nice try! But you do not need that command for this challenge'
        return True


def unblock_commands_with_mkdir_hint(line, list_of_commands):
    line = line.strip()
    if ("mkdir" in line and line not in list_of_commands):
        print (
            "Nearly there!  But you're trying to build something "
            "different from what was expected.  Try building something else."
        )

        return True

    elif ("mv" in line or "cd" in line) and \
            not line.strip() == 'mv --help':

        print 'Nice try! But you do not need that command for this challenge'
        return True
