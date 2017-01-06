# cave.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from linux_story.common import get_story_file

dark_room = {
    "name": "dark-room",
    "challenges": [
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0300
        },
        {
            "challenge": 35,
            "step": 1,
            "permissions": 0700
        }
    ],
    "children": [
        {
            "name": "sign",
            "contents": get_story_file("x-sign")
        }
    ]
}

cage_room = {
    "name": "cage",
    "challenges": [
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0500
        },
        {
            "challenge": 35,
            "step": 6,
            "permissions": 0700
        }
    ],
    "children": [
        {
            "name": "bird",
            "contents": get_story_file("bird"),
            "challenges": [
                {
                    "challenge": 36,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "scroll",
            "contents": get_story_file("scroll-cage"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 36,
                    "step": 1
                }
            ]
        }
    ]
}

locked_room = {
    "name": "locked-room",
    "challenges": [
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0600
        },
        {
            "challenge": 35,
            "step": 4,
            "permissions": 0700
        }
    ],
    "children": [
        {
            "name": "firework",
            "contents": get_story_file("firework-animation")
        },
        {
            "name": "sign",
            "contents": get_story_file("w-sign"),
            "challenges": [
                {
                    "challenge": 32,
                    "step": 1
                },
                {
                    "challenge": 33,
                    "step": 23
                }
            ]
        },
        {
            "name": "lighter",
            "contents": get_story_file("lighter"),
            "challenges": [
                {
                    "challenge": 32,
                    "step": 1
                },
                {
                    "challenge": 36,
                    "step": 4,
                    "permissions": 0755
                }
            ]
        }
    ]
}

chest = {
    "name": "chest",
    "children": [
        {
            "name": "riddle",
            "contents": get_story_file("riddle-cave")
        },
        {
            "name": "answer",
            "contents": get_story_file("answer-cave")
        }
    ],
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 37,
            "step": 2,
            "permissions": 0000
        },
        {
            "challenge": 37,
            "step": 5,
            "permissions": 0700
        }
    ]
}

cave = {
    "name": "cave",
    "children": [
        dark_room,
        cage_room,
        locked_room,
        chest,
        {
            "name": "sign",
            "contents": get_story_file("sign_cave")
        }
    ]
}