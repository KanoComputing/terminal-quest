
import os
import yaml
import sys

# from linux_story.common import HOME_FOLDER
HOME_FOLDER = os.path.expanduser('~')

current_dir = os.path.abspath(os.path.dirname(__file__))
config_dir = os.path.join(current_dir, "story_trees")
config_filepath = os.path.join(config_dir, "default_trees.yml")

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


# This whole structure has the problem of files needing unique names, unless
# you have a rename option, which feels very strange
# Ideally, we want a data structure like the one in challenges.yml:

# Mum:
#    challenges:
#        - challenge: 1
#          step: 1
#          path: "~/my-house/kitchen"

#        - challenge: 8
#          step: 1
#          exists: False

# But for the system, we want to look up for that challenge which files are
# needed.
# We can either look up for each file whether it exists, or we can retrive a
# the data for ONLY the requested challenge number


# Change this to a better defined dictionary

def get_default(challenge_number, step_number):
    tree = DefaultTree(challenge_number, step_number)
    return tree.story_dict


class DefaultTree():
    '''Returns the data about the file system and the relevent challenges/steps

    self.story_dict is a dictionary of the form:

    {
        filename_id: {
            {
                'challenge': 8,
                'step': 3,
                'path': '/path/to/file'
            }
       },
        filename_id2: {
           ...
        }
    }

    '''

    story_tree_directory = os.path.join(HOME_FOLDER, 'terminal-quest-test')

    def __init__(self, challenge_number, step_number):
        # Create the story tree directory if it doesn't already exist
        if not os.path.exists(self.story_tree_directory):
            os.mkdir(self.story_tree_directory)

        # This is a dictionary which can be processed by StoryFileTree class
        self.story_dict = {}

        # not sure whether to make into a class, or keep it functional
        self.create_directory_tree(challenge_number, step_number)
        self.get_relevant_challenge()

    def get_relevant_challenge(self):
        '''Order the array of dictiories by the challenge, and then step.
        We can then take the last element of the ordered dictionaries, and this
        will be the relevent challenge.
        '''

        for name, file_dict in self.tree.iteritems():

            if 'challenges' in file_dict:
                challenge_array = file_dict['challenges']

                sorted_challenges = sorted(
                    challenge_array, key=lambda k: (k['challenge'], k['step'])
                )

                # If the list is non empty,
                # only last element should be relevent
                if sorted_challenges:
                    self.story_dict[name] = {}
                    self.story_dict[name] = sorted_challenges[-1]

                    if 'name' in file_dict:
                        self.story_dict[name]['name'] = file_dict['name']

    def create_directory_tree(self, current_challenge, current_step):
        '''Go through the yaml, and take out the challenges that are greater
        than the ones we're interested in.
        '''

        current_challenge = int(current_challenge)
        current_step = int(current_step)

        self.tree = {}
        # Go through the config file

        stream = open(config_filepath)
        data = yaml.load(stream)

        for dict_id, data_dict in data.iteritems():

            # Filter relevent challenges in data_dict
            if 'challenges' in data_dict.keys():

                # If the challenges go above the challenge we're
                # considering, we can immediately block it and
                # return the last element
                stored_challenges = data_dict['challenges']
                relevant_challenges = []

                for challenge in stored_challenges:

                    # Only accept challenges that are <= to the current
                    # challenge.
                    # Anything above is irrelevant.
                    if challenge['challenge'] < current_challenge or \
                       (challenge['challenge'] == current_challenge and
                            challenge['step'] <= current_step):

                        # Only if these point apply do you add it to the
                        # tree.
                        relevant_challenges.append(challenge)

                data_dict['challenges'] = relevant_challenges

                # We don't have all the information yet, so we can't
                # reorder the elements yet

            # All file names
            filenames = dict_id.split(', ')
            for name in filenames:

                # if challenges in the data dictionary, remove all challenges
                # greater than the one we're considering now

                if name in self.tree.keys():
                    # Analyse tree[name] and try and blend the
                    # two together print challenge_dict['challenges']

                    if 'challenges' in self.tree[name]:
                        self.tree[name]['challenges'] += data_dict['challenges']
                    else:
                        self.tree[name]['challenges'] = data_dict['challenges']

                else:
                    self.tree[name] = data_dict

        return self.tree


if __name__ == "__main__":
    tree = DefaultTree()
