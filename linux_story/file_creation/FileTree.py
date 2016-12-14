# FileTree.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# This takes the file tree from a dictionary and creates it.

import filecmp
import os
import shutil
import stat


class FileTree:
    KEY_PERMISSIONS = "permissions"
    KEY_NAME = "name"
    KEY_CHILDREN = "children"
    KEY_OWNER = "owner"
    KEY_TYPE = "type"
    KEY_CONTENTS = "contents"
    KEY_CHALLENGES = "challenges"
    KEY_CHALLENGE = "challenge"
    KEY_STEP = "step"
    KEY_EXISTS = "exists"
    TYPE_DIR = "directory"
    TYPE_FILE = "file"
    DEFAULT_DIR_PERMISSIONS = 0755
    DEFAULT_FILE_PERMISSIONS = 0644

    def __init__(self, tree, end_dir):
        self.__tree = tree
        self.__end_dir = end_dir
        self.__create_dir(end_dir, 0755)

    def parse_complete(self, challenge, step):
        self.__clear_old_tree()
        self.__parse(self.__tree, self.__end_dir, challenge, step)

    def create_item(self, item_type, path, permissions, contents_path):
        path = os.path.join(self.__end_dir, path)
        self.__create_item(item_type, path, permissions, {self.KEY_CONTENTS: contents_path})

    def __clear_old_tree(self):
        revert_to_default_permissions(self.__end_dir)
        delete_item(self.__end_dir)
        os.mkdir(self.__end_dir)

    def __parse(self, tree, path, challenge, step):
        if "name" not in tree:
            raise Exception("No name for component in tree")

        challenge_data = self.__specs_for_challenge(challenge, step, tree)
        if not self.__exists_in_current_challenge(challenge_data):
            return

        path = os.path.join(path, tree[self.KEY_NAME])
        item_type = self.__get_item_type(tree)
        permissions = self.__get_permissions(challenge_data, item_type)
        self.__create_item(item_type, path, permissions, tree)

        if self.KEY_CHILDREN in tree:
            for child_tree in tree[self.KEY_CHILDREN]:
                self.__parse(child_tree, path, challenge, step)

    def __create_item(self, item_type, path, permissions, tree):
        parent_dir = os.path.normpath(os.path.join(path, ".."))

        if not os.path.exists(parent_dir):
            self.__create_dir(parent_dir, 0755)

        mode = os.stat(parent_dir).st_mode
        permissions_changed = self.__make_parent_writable(parent_dir, mode)

        if item_type == self.TYPE_DIR:
            self.__create_dir(path, permissions)
        elif item_type == self.TYPE_FILE:
            src_path = self.__get_contents_path(tree)
            self.__create_file(path, permissions, src_path)

        if permissions_changed:
            os.chmod(parent_dir, stat.S_IMODE(mode))

    def __exists_in_current_challenge(self, challenge_data):
        if self.KEY_CHALLENGE not in challenge_data and self.KEY_STEP not in challenge_data:
            return True
        if self.KEY_EXISTS in challenge_data and not challenge_data[self.KEY_EXISTS]:
            return False

        return True

    def __specs_for_challenge(self, challenge, step, tree):
        if self.KEY_CHALLENGES not in tree:
            return tree

        lower_bound_challenge = 1
        lower_bound_step = 1
        challenge_data = {}
        for challenge_dict in tree[self.KEY_CHALLENGES]:
            if self.KEY_CHALLENGE not in challenge_dict or self.KEY_STEP not in challenge_dict:
                raise Exception("missing challenge key in " + str(challenge_dict))
            poss_challenge = challenge_dict["challenge"]
            poss_step = challenge_dict["step"]

            if self.__challenge_step_earlier_or_equal(challenge, step, poss_challenge, poss_step):
                challenge_data = challenge_dict
                if self.__challenge_step_higher(lower_bound_challenge, lower_bound_step, poss_challenge, poss_step):
                    lower_bound_challenge = poss_challenge
                    lower_bound_step = poss_step

        if self.KEY_PERMISSIONS in tree:
            challenge_data[self.KEY_PERMISSIONS] = tree[self.KEY_PERMISSIONS]

        return challenge_data

    @staticmethod
    def __challenge_step_higher(challenge, step, poss_challenge, poss_step):
        return (poss_challenge > challenge) or (poss_challenge == challenge and poss_step > step)

    @staticmethod
    def __challenge_step_earlier_or_equal(challenge, step, poss_challenge, poss_step):
        return (poss_challenge <= challenge and poss_step <= step) or (poss_challenge < challenge)

    @staticmethod
    def __create_dir(path, permissions):
        if os.path.exists(path) and not os.path.isdir(path):
            raise Exception("File " + path + " exists and should be a directory")
        if not os.path.exists(path):  # check permissions
            os.mkdir(path, permissions)

    @staticmethod
    def __create_file(path, permissions, src_path):
        if os.path.exists(path) and os.path.isdir(path):
            raise Exception("File " + path + " exists and should be a file")
        if os.path.exists(path) and not filecmp.cmp(path, src_path, shallow=False):
            os.remove(path)

        shutil.copyfile(src_path, path)
        os.chmod(path, permissions)

    @staticmethod
    def __make_parent_writable(parent_dir, mode):
        if bool(mode & stat.S_IWUSR) and bool(mode & stat.S_IXUSR):
            return False
        else:
            os.chmod(parent_dir, 0755)
            return True

    def __get_permissions(self, challenge_data, item_type):
        permissions = self.__get_default_permissions(item_type)
        if self.KEY_PERMISSIONS in challenge_data:
            permissions = challenge_data[self.KEY_PERMISSIONS]
        return permissions

    def __get_default_permissions(self, type):
        if type == self.TYPE_DIR:
            return self.DEFAULT_DIR_PERMISSIONS
        elif type == self.TYPE_FILE:
            return self.DEFAULT_FILE_PERMISSIONS

    def __get_item_type(self, tree):
        if self.KEY_CHILDREN in tree or (
                self.KEY_TYPE in tree and tree[self.KEY_TYPE] == self.TYPE_DIR):
            return self.TYPE_DIR
        else:
            return self.TYPE_FILE

    def __get_owner(self, tree):
        owner = self.__get_default_owner()
        if self.KEY_OWNER in tree:
            owner = tree[self.KEY_OWNER]
        return owner

    @staticmethod
    def __get_default_owner():
        return os.environ['LOGNAME']

    def __get_contents_path(self, tree):
        if self.KEY_CONTENTS not in tree:
            raise Exception("No contents associated with the file: " + tree["name"])
        return tree[self.KEY_CONTENTS]


def delete_item(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def revert_to_default_permissions(filesystem):
    for root, dirs, files in os.walk(filesystem):
        for d in dirs:
            path = os.path.join(root, d)
            os.chmod(path, 0755)
        for f in files:
            path = os.path.join(root, f)
            os.chmod(path, 0644)


def get_oct_permissions(path):
    return oct(os.stat(path).st_mode & 0777)


def get_int_permissions(path):
    return int(os.stat(path).st_mode & 0777)