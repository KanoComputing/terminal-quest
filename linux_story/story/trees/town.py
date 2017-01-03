# town.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from linux_story.common import get_story_file
from hidden_shelter import hidden_shelter
from east import east


grumpy_man = {
    "name": "grumpy-man",
    "contents": get_story_file("grumpy-man"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1
        },
        {
            "challenge": 8,
            "step": 1,
            "exists": False
        }
    ]
}

young_girl = {
    "name": "young-girl",
    "contents": get_story_file("young-girl"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1
        },
        {
            "challenge": 8,
            "step": 2,
            "exists": False
        }
    ]
}

little_boy = {
    "name": "little-boy",
    "contents": get_story_file("little-boy"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1
        },
        {
            "challenge": 8,
            "step": 3,
            "exists": False
        }
    ]
}

mayor = {
    "name": "Mayor",
    "contents": get_story_file("Mayor"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1
        },
        {
            "challenge": 8,
            "step": 6,
            "exists": False
        }
    ]
}

note_town = {
    "name": "note",
    "contents": get_story_file("note_town"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 8,
            "step": 6
        },
        {
            "challenge": 10,
            "step": 1,
            "exists": False
        }
    ]
}

dog_town = {
    "name": "dog",
    "contents": get_story_file("dog"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 11,
            "step": 6
        },
        {
            "challenge": 12,
            "step": 2,
            "exists": False
        }
    ]
}

eleanor_town = {
    "name": "Eleanor",
    "contents": get_story_file("Eleanor"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 11,
            "step": 6
        },
        {
            "challenge": 12,
            "step": 1,
            "exists": False
        }
    ]
}

town = {
    "name": "town",
    "children": [
        hidden_shelter,
        grumpy_man,
        young_girl,
        little_boy,
        note_town,
        mayor,
        east,
        dog_town,
        eleanor_town
    ]
}
