# commands_fake.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Terminal commands which are emulated


import os
import getpass
from kano.logging import logger


def cd(real_path, line, has_access=True):
    if not has_access:
        # Could simplify this to "Permission denied"
        print "-bash: cd: {}: Permission denied".format(line)
        return

    tq_file_system = os.path.join(os.path.expanduser('~'), '.linux-story')

    if not line:
        new_path = tq_file_system
    else:
        if line.startswith('~'):
            new_line = line.replace('~', '~/.linux-story')
            new_path = os.path.expanduser(new_line)
        else:
            new_path = os.path.join(real_path, line)

            # We use os.path.abspath so we don't get paths
            # like ~/my-house/../my-house
            new_path = os.path.abspath(new_path)

        if not os.path.exists(new_path) or not os.path.isdir(new_path):
            new_path = real_path

    if new_path[-1] == '/':
        new_path = new_path[:-1]
    return new_path


def sudo(real_path, line, counter=0, success_cb=None, *cb_args):
    '''
    Ask the user for their password, and do not show answer.
    If the user is successful, execute success_cb with success_args passed
    '''

    if counter == 3:
        print "sudo: 3 incorrect password attempts"
        return

    user = getpass.getuser()
    pswd = getpass.getpass('[sudo] password for {}:'.format(user))

    # For now hardcode the password?
    if pswd != "kano":
        print "Sorry, try again."
        counter += 1
        return sudo(real_path, line, counter)

    logger.debug("successfully entered pswd = {}".format(pswd))
    logger.debug("calling success cb = {}".format(cb_args))
    if success_cb:
        success_cb(*cb_args)
