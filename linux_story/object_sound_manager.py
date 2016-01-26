# object_sound_manager.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Sound Manager for ASCII game objects


import traceback

from kano.logging import logger

from linux_story.helper_functions import play_sound


class ObjectSoundManager(object):
    """
    This class contains the sound playback for both the commands being run
    and also for the story text being typed.

    The dicts below map an ASCII art file or a script file to a sound name.
    """

    # for `cat <object>`
    cat_object_sound = {
        'alarm': 'alarm',
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
    run_object_sound = {
        'best-horn-in-the-world.sh': 'horn',
        'best-shed-maker-in-the-world.sh': 'mkdir'
    }

    # for Storybook text
    story_text_sound = {
        'New Spell': 'new_command',
        'Ding. Dong.': 'bell'
    }

    def play_cat(self, object_name):
        """
        Play the sound specific to the object_name in a CAT context.

        Args:
            object_name (str): an ASCII file name
        """

        try:
            play_sound(self.cat_object_sound[object_name], background=False)
        except KeyError:
            pass  # it's ok, there just isn't a sound in the dict for this object

        except Exception:
            logger.error('Unexpected error while playing sound. object_name is {} {}'
                         .format(object_name, traceback.format_exc()))

    def play_mv(self, object_name):
        """
        Play the sound specific to the object_name in a MV context.

        Args:
            object_name (str): an ASCII file name
        """

        try:
            play_sound(self.mv_object_sound[object_name], background=False)
        except KeyError:
            pass  # it's ok, there just isn't a sound in the dict for this object

        except Exception:
            logger.error('Unexpected error while playing sound. object_name is {} {}'
                         .format(object_name, traceback.format_exc()))

    def play_mkdir(self):
        """
        Play the sound specific to the MKDIR command when run.
        """

        try:
            play_sound('mkdir')

        except Exception:
            logger.error('Unexpected error while playing sound {}'
                         .format(traceback.format_exc()))

    def play_nano(self):
        """
        Play the sound specific to the NANO command when run.
        """

        try:
            play_sound('paper')

        except Exception:
            logger.error('Unexpected error while playing sound {}'
                         .format(traceback.format_exc()))

    def play_run(self, script):
        """
        Play the sound specific to the script when it's run.

        Args:
            script (str): the script filename
        """

        try:
            play_sound(self.run_object_sound[script], background=False)
        except KeyError:
            pass  # it's ok, there just isn't a sound in the dict for this object

        except Exception:
            logger.error('Unexpected error while playing sound. script is {} {}'
                         .format(script, traceback.format_exc()))

    def play_story(self, story_text):
        """
        Play the sound for the key_words in the story_text.

        It checks which of the key_words are at the beginning of the story_text
        and plays the corresponding sound, e.g. 'Ding. Dong.' in the story plays 'bell'.

        Args:
            story_text (str): an excerpt of the story text in the challenges
        """

        for key_words, sound_name in self.story_text_sound.items():
            if story_text.startswith(key_words):
                try:
                    play_sound(sound_name)

                except Exception:
                    logger.error('Unexpected error while playing sound. story_text is {}'
                                 ' {}'.format(story_text, traceback.format_exc()))
