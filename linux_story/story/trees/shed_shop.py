# shed-shop.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from linux_story.common import get_story_file

shed_shop = {
    "name": "shed-shop",
    "children": [
        {
            "name": "Eleanor",
            "contents": get_story_file("Eleanor"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 24,
                    "step": 4
                },
                {
                    "challenge": 26,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 27,
                    "step": 1
                },
                {
                    "challenge": 28,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "Bernard",
            "contents": get_story_file("Bernard"),
            "challenges": [
                {
                    "challenge": 23,
                    "step": 1
                },
                {
                    "challenge": 30,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "Bernards-hat",
            "contents": get_story_file("bernards-hat"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 30,
                    "step": 1
                }
            ]
        },
        {
            "name": "best-shed-maker-in-the-world.sh",
            "contents": get_story_file("best-shed-maker-in-the-world.sh"),
            "challenges": [
                {
                    "challenge": 23,
                    "step": 1,
                    "permissions": 0755
                }
            ]
        },
        {
            "name": "best-horn-in-the-world.sh",
            "contents": get_story_file("best-horn-in-the-world-incorrect.sh"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 23,
                    "step": 1,
                    "permissions": 0755
                },
                {
                    "challenge": 27,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "best-horn-in-the-world.sh",
            "contents": get_story_file("best-horn-in-the-world-correct.sh"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 27,
                    "step": 3,
                    "permissions": 0755
                }
            ]
        },
        {
            "name": "basement",
            "type": "directory",
            "children": [
                {
                    "name": "bernards-diary-1",
                    "contents": get_story_file("bernards-diary-1"),
                    "challenges": [
                        {
                            "challenge": 23,
                            "step": 1
                        }
                    ]
                },
                {
                    "name": "bernards-diary-2",
                    "contents": get_story_file("bernards-diary-2"),
                    "challenges": [
                        {
                            "challenge": 23,
                            "step": 1
                        }
                    ]
                },
                {
                    "name": "photocopier.sh",
                    "contents": get_story_file("photocopier.sh"),
                    "permissions": 0755,
                    "challenges": [
                        {
                            "challenge": 23,
                            "step": 1
                        }
                    ]
                }
            ]
        }
    ]
}
