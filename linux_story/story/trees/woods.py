# woods.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from cave import cave
from clearing import clearing
from rabbithole import rabbithole
from linux_story.common import get_story_file


thicket = {
    "name": "thicket",
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
    ],
    "children": [
        rabbithole,
        {
            "name": "Rabbit",
            "contents": get_story_file("Rabbit"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 40,
                    "step": 1
                },
                {
                    "challenge": 42,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "note",
            "contents": get_story_file("note_rabbithole"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 40,
                    "step": 1
                },
                {
                    "challenge": 42,
                    "step": 1,
                    "exists": False
                }
            ]
        }
    ]
}


woods = {
    "name": "woods",
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
    ],
    "children": [
        clearing,
        cave,
        thicket,
        {
            "contents": get_story_file("note_woods"),
            "name": "note",
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 41,
                    "step": 2
                }
            ]
        },
    ]
}