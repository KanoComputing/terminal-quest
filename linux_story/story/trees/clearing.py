# clearing.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from linux_story.common import get_story_file

house = {
    "name": "house",
    "children": [
        {
           "name": "swordmaster",
            "contents": get_story_file("swordmaster"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 32,
                    "step": 1
                },
                {
                    "challenge": 43,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "note",
            "contents": get_story_file("note_woods"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 40,
                    "step": 1
                }
            ]
        }
    ],
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0000
        },
        {
            "challenge": 33,
            "step": 32,
            "permissions": 0700,
        }
    ]
}

clearing = {
    "name": "clearing",
    "children": [
        house,
        {
            "name": "signpost",
            "contents": get_story_file("signpost")
        }
    ],
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 32,
            "step": 1
        }
    ]
}