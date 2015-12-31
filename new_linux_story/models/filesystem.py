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


class ChildInFileException(Exception):
    pass


class CannotNavigateToPathException(Exception):
    pass


class FirstPathElementMismatchException(Exception):
    pass


class NonUniqueFileException(Exception):
    pass


class PathDoesNotExistException(Exception):
    pass


class NoPathException(Exception):
    pass


class FileSystemTypeMissing(Exception):
    pass


class Node(object):
    def __init__(self, path, name, permissions, owner):
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


class FileObject(Node):
    def __init__(self, path, name, content, permissions, owner):
        super(FileObject, self).__init__(path, name, permissions, owner)

        self._type = "file"

        # Contents of file
        self._content = ""

    @property
    def content(self):
        return self._content

    def _set_content_from_file(self, file):
        f = open(file, 'r')
        self._content = f
        f.close()


class Directory(Node):
    def __init__(self, path, name, children, permissions, owner):
        super(Directory, self).__init__(path, name, permissions, owner)

        self._type = "directory"

        self._children = children

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)

    def get_children_names(self):
        return [c.name for c in self._children]


class FileSystem(object):
    '''
    This is the filesystem in memory
    '''

    def __init__(self, filesystem):
        # start off filesystem with ~
        self._home = Directory("~", "~", [], 0755, os.environ["USER"])
        self._filesystem = filesystem
        self.make_filesystem_from_config(self._filesystem)

    def add_file_at_path_with_content_file(self, path, name, content_file,
                                           permissions, owner):
        '''
        Returns True if successfully added file to filesystem, False otherwise
        '''
        (exists, d) = self.path_exists(path)

        if exists and d.type == "directory":
            d.add_child(FileObject(path, name, content_file, permissions,
                                   owner))
            return True

        return False

    def add_file_at_path_with_content(self, path, name, content,
                                      permissions, owner):
        '''
        Returns True if successfully added file to filesystem, False otherwise
        '''
        print "content = {}".format(content)
        (exists, d) = self.path_exists(path)

        if exists and d.type == "directory":
            d.add_child(FileObject(path, name, content, permissions,
                                   owner))
            return True

        return False

    def add_dir_at_path(self, path, name, permissions, owner):
        '''
        Returns True if successfully added dir to filesystem, False otherwise
        '''
        (exists, d) = self.path_exists(path)

        if exists and d.type == "directory":
            d.add_child(Directory(path, name, [], permissions, owner))
            return True

        return False

    def get_all_at_path(self, path):
        (exists, d) = self.path_exists(path)

        if not exists:
            raise PathDoesNotExistException

        if exists and d.type == "directory":
            return sorted(d.children, key=lambda k: k.name)

    def get_names_at_path(self, path, ftype):
        '''
        ftype = "files", "dirs" or "all"
        '''

        if ftype == "all":
            files = self.get_all_at_path(path)
        elif ftype == "files":
            files = self.get_files_at_path(path)
        elif ftype == "dirs":
            files = self.get_dirs_at_path(path)
        else:
            raise FileSystemTypeMissing

        names = []
        # This should preserve the order
        for f in files:
            names.append(f.name)
        return names

    def get_all_names_at_path(self, path):
        return self.get_names_at_path(path, "all")

    def get_filenames_at_path(self, path):
        return self.get_names_at_path(path, "files")

    def get_dirnames_at_path(self, path):
        return self.get_names_at_path(path, "dirs")

    def get_files_at_path(self, path):
        all_files = self.get_all_at_path(path)
        files = [f for f in all_files if f.type == "file"]
        # Sort by name
        files = sorted(files, key=lambda k: k.name)
        return files

    def get_dirs_at_path(self, path):
        all_files = self.get_all_at_path(path)
        dirs = [f for f in all_files if f.type == "directory"]
        dirs = sorted(dirs, key=lambda k: k.name)
        return dirs

    def get_permissions_of_path(self, path):
        (exists, d) = self.path_exists(path)
        if exists:
            return d.permissions

    # Fighting the data structure?
    def path_exists(self, path):
        '''
        :param path: file path
        :type path: string

        :returns: (if_path_exists, tree)
        :rtype: (bool, dictionary)
        '''
        if not path:
            raise NoPathException

        # Remove .. and redundant slashes
        path = os.path.normpath(path)
        # Strip the empty elements
        levels = path.split("/")
        levels = filter(None, levels)
        f = self._home

        # the first level must be ~
        if not f.name == levels[0]:
            return (False, None)

        if len(levels) == 1:
            return (True, f)

        levels = levels[1:]

        for n in range(len(levels)):
            matching_elements = [child for child in f.children
                                 if child.name == levels[n]]
            # filesystem has not been written correctly
            # TODO: Does this check need to be here?
            if len(matching_elements) > 1:
                raise NonUniqueFileException
            elif len(matching_elements) == 0:
                # Path does not exist
                return (False, None)
            else:
                f = matching_elements[0]

                if n < len(levels) - 1:
                    # TODO: Maybe this check shouldn't be here
                    if not f.type == "directory":
                        raise ChildInFileException

        return (True, f)

    def make_filesystem_from_config(self, filesystem):
        '''
        Make the filesystem in memory
        '''
        def recursive_bit(path, filesystem):
            for f in filesystem:
                name = f["name"]
                objtype = f["type"]

                if objtype == "file":
                    self._add_file_config_to_filesystem(path, f)

                elif objtype == "directory":
                    self._add_dir_config_to_filesystem(path, f)

                    if "children" in f:
                        children = f["children"]
                        recursive_bit(os.path.join(path, name), children)

        recursive_bit("~", filesystem)

    def _add_file_config_to_filesystem(self, path, f):
        name = f["name"]
        permissions = 0644
        owner = os.environ["USER"]

        # TODO: repeated owner logic for dir and file
        if "permissions" in f:
            permissions = f["permissions"]

        if "owner" in f:
            owner = f["owner"]

        if "children" in f:
            raise ChildInFileException

        if "content_file" in f:
            content_file = f["content_file"]
            self.add_file_at_path_from_file(path,
                                            name,
                                            content_file,
                                            permissions,
                                            owner)
        elif "content" in f:
            content = f["content"]
            self.add_file_at_path_with_content(path,
                                               name,
                                               content,
                                               permissions,
                                               owner)
        else:
            self.add_file_at_path_with_content(path,
                                               name,
                                               "",
                                               permissions,
                                               owner)

    def _add_dir_config_to_filesystem(self, path, f):
        name = f["name"]
        permissions = 0755
        owner = os.environ["USER"]

        if "permissions" in f:
            permissions = f["permissions"]

        if "owner" in f:
            owner = f["owner"]

        self.add_dir_at_path(path, name, permissions, owner)
