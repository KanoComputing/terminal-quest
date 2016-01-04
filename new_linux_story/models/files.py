#!/usr/bin/env python

# files.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The following classes emulate files and directories


class NoParentError(Exception):
    pass


class OverwritePathException(Exception):
    pass


class CannotNavigateToPathException(Exception):
    pass


class FirstPathElementMismatchException(Exception):
    pass


class Node(object):
    '''
    This contains common elements between the FileObject and Directory classes
    '''
    def __init__(self, path, name, permissions, owner, start_challenge,
                 start_step, end_challenge, end_step):
        # Full path. Maybe calculate this from the tree?
        self._path = path

        # this is the filename
        self._name = name

        # Permissions. Useful for "ls -l" and chmod.
        self._permissions = permissions

        # Owner for when the owner is root
        self._owner = owner

        # For now, assume the group and owner are the same
        self._group = owner

        self._type = ""

        # challenges the object should exists for
        self._start_challenge = start_challenge
        self._end_challenge = end_challenge
        self._start_step = start_step
        self._end_step = end_step

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def permissions(self):
        return self._permissions

    @property
    def type(self):
        return self._type

    @property
    def owner(self):
        return self._owner

    @property
    def group(self):
        return self._group

    @property
    def start_challenge(self):
        return self._start_challenge

    @property
    def end_challenge(self):
        return self._end_challenge

    @property
    def start_step(self):
        return self._start_step

    @property
    def end_step(self):
        return self._end_step

    # TODO: has_read_permission, has_execute_permission and
    # has_write_permission are fairly similar. Combine in one function.
    def has_read_permission(self, user):
        '''
        Check whether the user has read permissions.

        :param user: name of user trying to read the contents
        :type user: string
        :returns: whether user has read permission
        :rtype: bool
        '''
        # first check permissions others who are not user or group have.
        other_bit = int(oct(self._permissions)[-1])
        if other_bit >= 4:
            return True

        if not len(oct(self._permissions)) >= 3:
            return False

        group_bit = int(oct(self._permissions)[-2])
        if self._group == user and group_bit >= 4:
            return True

        if not len(oct(self._permissions)) == 4:
            return False

        owner_bit = int(oct(self._permissions)[1])
        if self._owner == user and owner_bit >= 4:
            return True

        return False

    def has_execute_permission(self, user):
        '''
        Check whether the user has execute permissions.

        :param user: name of user
        :type user: string
        :returns: whether user has execute permission.
        :rtype: bool
        '''
        other_bit = int(oct(self._permissions)[-1])
        if other_bit % 2 == 1:
            return True

        if not len(oct(self._permissions)) >= 3:
            return False

        group_bit = int(oct(self._permissions)[-3])
        if self._group == user and group_bit % 2 == 1:
            return True

        if not len(oct(self._permissions)) == 4:
            return False

        owner_bit = int(oct(self._permissions)[1])
        if self._owner == user and owner_bit % 2 == 1:
            return True

        return False

    def has_write_permission(self, user):
        '''
        Check whether the user has write permissions.

        :param user: name of user
        :type user: string
        :returns: whether user has write permission.
        :rtype: bool
        '''
        other_bit = int(oct(self._permissions)[-1])
        if other_bit % 4 >= 2:
            return True

        if not len(oct(self._permissions)) >= 3:
            return False

        group_bit = int(oct(self._permissions)[-3])
        if self._group == user and group_bit % 4 >= 2:
            return True

        if not len(oct(self._permissions)) == 4:
            return False

        owner_bit = int(oct(self._permissions)[1])
        if self._owner == user and owner_bit % 4 >= 2:
            return True

        return False

    def exists_in_challenge(self, challenge, step):
        '''
        Check the node object exists in the file system for the challenge/step.

        :param challenge: challenge number
        :type challenge: int
        :param step: step number
        :type challenge: int
        :returns: whether the node object exists
        :rtype: bool
        '''
        if challenge < self.start_challenge:
            return False
        elif challenge > self.end_challenge and self.end_challenge != -1:
            return False
        elif challenge == self.start_challenge and step < self.start_step:
            return False
        elif challenge == self.end_challenge and step > self.end_step \
                and self.end_step != -1:
            return False
        else:
            return True


class FileObject(Node):
    '''
    This class represents a file in a linux filesystem
    '''
    def __init__(self, path, name, content, permissions, owner,
                 start_challenge, start_step, end_challenge, end_step):
        super(FileObject, self).__init__(path, name, permissions, owner,
                                         start_challenge, start_step,
                                         end_challenge, end_step)

        self._type = "file"

        # Contents of file
        self._content = content

    @property
    def content(self):
        return self._content


class Directory(Node):
    '''
    This class represents a directory in a linux filesystem
    '''
    def __init__(self, path, name, children, permissions, owner,
                 start_challenge, start_step, end_challenge, end_step):
        super(Directory, self).__init__(path, name, permissions, owner,
                                        start_challenge, start_step,
                                        end_challenge, end_step)

        self._type = "directory"

        self._children = children

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)
        self._children.sort(key=lambda x: x.name)

    def get_children_names(self):
        return [c.name for c in self._children]
