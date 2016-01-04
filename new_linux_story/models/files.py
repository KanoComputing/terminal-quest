import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


class NoParentError(Exception):
    pass


class OverwritePathException(Exception):
    pass


class CannotNavigateToPathException(Exception):
    pass


class FirstPathElementMismatchException(Exception):
    pass


class Node(object):
    def __init__(self, path, name, permissions, owner, start_challenge,
                 start_step, end_challenge, end_step):
        # Full path. Maybe calculate this from the tree?
        self._path = path

        # this is the filename
        self._name = name

        # Parent directory
        # self._parent = parent

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

    # @property
    # def parent(self):
    #   return self._parent

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

    def has_read_permission(self, user):

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
