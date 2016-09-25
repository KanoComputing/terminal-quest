# sound_manager.py
#
# Copyright (C) 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Sound Manager for ASCII game objects


import os
import traceback

from kano.utils import play_sound as play_sound_toolset
from kano.logging import logger

from linux_story.common import sounds_dir


class SoundManager(object):
    """
    This class contains the sound playback for both the commands being run
    and also for the story text being typed.

    The dicts below map an ASCII art file or a script file to a sound name.
    """

    # for `cat <object>`
    cat_object_sound = {
        'Daisy': 'bull',
        'Cobweb': 'cobweb',
        'dog': 'dog',
        'newspaper': 'paper',
        'comic-book': 'paper',
        'note': 'paper',
        'LS': 'paper',
        'CAT': 'paper',
        'MV': 'paper',
        'ECHO': 'paper',
        'MKDIR': 'paper',
        'NANO': 'paper',
        'photocopier.sh': 'paper',
        'best-horn-in-the-world.sh': 'paper',
        'best-shed-maker-in-the-world.sh': 'paper',
        'bernards-diary-1': 'paper',
        'bernards-diary-2': 'paper',
        'mums-diary': 'paper',
        'alice-and-wonderland': 'paper',
        'watership-down': 'paper',
        'redwall': 'paper',
        'map': 'paper',
        'Trotter': 'trotter'
    }

    # for `mv <object>`
    mv_object_sound = {
        'Daisy': 'bull',
        'dog': 'dog',
        'Cobweb': 'cobweb',
        'Trotter': 'trotter'
    }

    # for `./<script>`
    script_object_sound = {
        'best-horn-in-the-world.sh': 'horn',
        'best-shed-maker-in-the-world.sh': 'mkdir'
    }

    # for Storybook text
    story_text_sound = {
        'New Spell': 'new_command',
        'Ding. Dong.': 'bell'
    }

    def on_command_run(self, command_args):
        """
        Play the appropriate sound for the command and it's args.

        It expects the command to be on the first index in the list and it's args
        after it. It also handles scripts (which here all end in .sh).

        Args:
            command_args (list) - contains a terminal command args as strings
        """

        if not command_args:
            return

        try:
            if command_args[0] == 'cat':
                last_object_name = command_args[-1].rsplit(os.sep, 1)[-1]
                self._play_cat(last_object_name)

            elif command_args[0] == 'mv':
                first_object_name = command_args[1].rsplit(os.sep, 1)[-1]
                self._play_mv(first_object_name)

            elif command_args[0] == 'mkdir':
                self._play_mkdir()

            elif command_args[0] == 'nano':
                self._play_nano()

            elif command_args[0].endswith('.sh'):
                self._play_script(command_args[0])

        except Exception:
            logger.error('Unexpected error on_command_run. command_args is {}.\n{}'
                         .format(command_args, traceback.format_exc()))

    def on_typing_story_text(self, story_text):
        """
        Play the sound for the key_words in the story_text.

        It checks which of the key_words are at the beginning of the story_text
        and plays the corresponding sound, e.g. 'Ding. Dong.' in the story plays 'bell'.

        Args:
            story_text (str) - an excerpt of the story text in the challenges
        """

        for key_words, sound_name in self.story_text_sound.items():
            if story_text.startswith(key_words):
                try:
                    self.play_sound(sound_name)
                    break

                except Exception:
                    logger.error('Unexpected error while playing sound. story_text is {}'
                                 ' {}'.format(story_text, traceback.format_exc()))

    def play_sound(self, sound_name, background=True):
        """
        Play a game sound in blocking or unblocking mode.

        Args:
            sound_name (str) - sound file name without extension, e.g. 'bell'
        """

        sound_path = os.path.join(sounds_dir, sound_name + '.wav')
        play_sound_toolset(sound_path, background=background)

    def _play_cat(self, object_name):
        """
        Play the sound specific to the object_name in a CAT context.

        Args:
            object_name (str) - an ASCII file name
        """

        try:
            self.play_sound(self.cat_object_sound[object_name], background=False)
        except KeyError:
            pass  # it's ok, there just isn't a sound in the dict for this object

        except Exception:
            logger.error('Unexpected error while playing sound. object_name is {} {}'
                         .format(object_name, traceback.format_exc()))

    def _play_mv(self, object_name):
        """
        Play the sound specific to the object_name in a MV context.

        Args:
            object_name (str) - an ASCII file name
        """

        try:
            self.play_sound(self.mv_object_sound[object_name], background=False)
        except KeyError:
            pass  # it's ok, there just isn't a sound in the dict for this object

        except Exception:
            logger.error('Unexpected error while playing sound. object_name is {} {}'
                         .format(object_name, traceback.format_exc()))

    def _play_mkdir(self):
        """
        Play the sound specific to the MKDIR command when run.
        """

        try:
            self.play_sound('mkdir')

        except Exception:
            logger.error('Unexpected error while playing sound {}'
                         .format(traceback.format_exc()))

    def _play_nano(self):
        """
        Play the sound specific to the NANO command when run.
        """

        try:
            self.play_sound('paper')

        except Exception:
            logger.error('Unexpected error while playing sound {}'
                         .format(traceback.format_exc()))

    def _play_script(self, script):
        """
        Play the sound specific to the script when it's run.

        Args:
            script (str) - the script filename with extension
        """

        try:
            self.play_sound(self.script_object_sound[script], background=False)
        except KeyError:
            pass  # it's ok, there just isn't a sound in the dict for this object

        except Exception:
            logger.error('Unexpected error while playing sound. script is {} {}'
                         .format(script, traceback.format_exc()))
