# common.py

# This would contain all the common names across the OS

import os

# setting up directories
current_dir = os.path.abspath(os.path.dirname(__file__))

# media dir
media_local = os.path.join(current_dir, '../media')
media_usr = '/usr/share/linux-story/media'

if os.path.exists(media_local):
    common_media_dir = media_local
elif os.path.exists(media_usr):
    common_media_dir = media_usr
else:
    raise Exception('Neither local nor usr media dir found!')

css_dir = os.path.join(current_dir, 'gtk3', 'css')

# Constants

# /home/user/
home_folder = os.path.expanduser('~')

# This is where the filetree that the user interacts with.
tq_file_system = os.path.join(home_folder, '.linux-story')

# The contents of this folder are backed up online
tq_backup_folder = os.path.join(home_folder, 'Terminal-Quest-content')


# This is the yaml file that we store the state of the current file system in
# The problem with this system is we don't have the contents of the file.
# Can we save the whole file tree?  Surely that's quicker.
def create_tq_backup_tree_path(challenge, step):
    '''Get the file path for the saved tree of the right challenge/step
    combination.
    '''
    if not os.path.exists(tq_backup_folder):
        os.mkdir(tq_backup_folder)

    filename = "challenge_" + str(challenge) + "_step_" + str(step) + ".yml"
    # If we need to make the file exist
    # open(filename, 'a').close()
    return os.path.join(tq_backup_folder, filename)


def get_tq_backup_tree_path(challenge, step):
    '''Get the last saved state which is applicable for the
    '''
    if not os.path.exists(tq_backup_folder):
        os.mkdir(tq_backup_folder)

    contents = os.listdir(tq_backup_folder)

    # Save states take the form of challenge_num_step_num
    relevant_save_states = []

    for f in contents:
        f_elements = f.split('_')
        if f.startswith("challenge") and len(f_elements) == 4:
            f_challenge = int(f_elements[1])
            f_step = int(f_elements[3])

            if f_challenge < challenge or \
               (f_challenge == challenge and
                    f_step <= step):

                f_dict = {"challenge": f_challenge, "step": f_step, "path": f}
                relevant_save_states.append(f_dict)

    if relevant_save_states:
        sorted_challenges = sorted(
            relevant_save_states, key=lambda k: (k['challenge'], k['step'])
        )
        print sorted_challenges
        save_state = sorted_challenges[-1]
        return os.path.join(tq_backup_folder, save_state)
