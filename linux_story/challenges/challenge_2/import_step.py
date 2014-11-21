import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)
        print sys.path


from linux_story.challenges.challenge_2.steps import Step1


def hello():
	print "hello"


hello()
