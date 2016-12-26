from linux_story.common import fake_home_dir


class PlayerLocation:
    def __init__(self, start_dir, end_dir):
        self.__fake_path = start_dir
        self.__end_dir = end_dir

    def get_fake_path(self):
        return self.__fake_path

    def get_real_path(self):
        return generate_real_path(self.__fake_path)

    def set_fake_path(self, fake_path):
        self.__fake_path = fake_path

    def set_real_path(self, real_path):
        self.__fake_path = generate_fake_path(real_path)

    def get_end_dir(self):
        return self.__end_dir

    def set_end_dir(self, end_dir):
        self.__end_dir = end_dir

    def is_at_end_dir(self):
        return self.__end_dir == self.__fake_path


def generate_real_path(fake_path):
    return fake_path.replace('~', fake_home_dir)


def generate_fake_path(real_path):
    return real_path.replace(fake_home_dir, '~')
