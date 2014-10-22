#!/usr/bin/env python

from distutils.core import setup
import os


# gets all directories from the directory in linux_story
def recursively_get_dirs(start_dir):
    start_path = os.path.join("./linux_story", start_dir)
    #dir_paths = [dir.replace("./linux_story/", "") + '/*' for dir, _, _ in os.walk(start_path)]
    paths = []

    for root, dir, files in os.walk(start_path):
        for f in files:
            file_path = os.path.join(root, f)
            file_path = file_path.replace("./linux_story/", "")
            paths.append(file_path)

    print paths
    return paths


file_system = recursively_get_dirs("file-system")
data = recursively_get_dirs("data")
animation = recursively_get_dirs("animation")


setup(name='Linux Story',
      version='1.2',
      description='Story to teach people basic Linux commands',
      author='Team Kano',
      author_email='dev@kano.me',
      url='https://github.com/KanoComputing/linux-tutorial',
      packages=['linux_story'],
      package_dir={'linux_story': 'linux_story'},
      scripts=['bin/linux-story'],
      package_data={'linux_story': file_system + data + animation}
      )

