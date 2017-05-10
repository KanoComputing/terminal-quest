# farm.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from linux_story.common import get_story_file

shelter = {
    "name": ".shelter",
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 21,
            "step": 7
        }
    ],
    "children": [
        {
            "name": "Cobweb",
            "contents": get_story_file("Cobweb"),
            "challenges": [
                {
                    "challenge": 21,
                    "step": 10
                }
            ]
        },
        {
            "name": "Trotter",
            "contents": get_story_file("Trotter"),
            "challenges": [
                {
                    "challenge": 21,
                    "step": 10
                }
            ]
        },
        {
            "name": "Daisy",
            "contents": get_story_file("Daisy"),
            "challenges": [
                {
                    "challenge": 21,
                    "step": 10
                }
            ]
        },
        {
            "name": "Ruth",
            "contents": get_story_file("Ruth"),
            "challenges": [
                {
                    "challenge": 21,
                    "step": 10
                }
            ]
        }
    ]
}


farm = {
    "name": "farm",
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 17,
            "step": 1
        }
    ],
    "children": [
        {
            "name": "barn",
            "challenges": [
                {
                    "challenge": 17,
                    "step": 1
                }
            ],
            "children": [
                shelter,
                {
                    "name": "Cobweb",
                    "contents": get_story_file("Cobweb"),
                    "challenges": [
                        {
                            "challenge": 21,
                            "step": 10
                        }
                    ]
                },
                {
                    "name": "Trotter",
                    "contents": get_story_file("Trotter"),
                    "challenges": [
                        {
                            "challenge": 21,
                            "step": 10
                        }
                    ]
                },
                {
                    "name": "Daisy",
                    "contents": get_story_file("Daisy"),
                    "challenges": [
                        {
                            "challenge": 21,
                            "step": 10
                        }
                    ]
                },
                {
                    "name": "Ruth",
                    "contents": get_story_file("Ruth"),
                    "challenges": [
                        {
                            "challenge": 21,
                            "step": 10
                        }
                    ]
                }
            ]
        },
        {
            "name": "farmhouse",
            "children": [
                {
                    "name": "bed",
                    "contents": get_story_file("bed_farmhouse")
                }
            ]
        },
        {
            "name": "toolshed",
            "children": [
                {
                    "name": "MKDIR",
                    "contents": get_story_file("MKDIR")
                },
                {
                    "name": "spanner",
                    "contents": get_story_file("spanner")
                },
                {
                    "name": "hammer",
                    "contents": get_story_file("hammer")
                },
                {
                    "name": "saw",
                    "contents": get_story_file("saw")
                },
                {
                    "name": "tape-measure",
                    "contents": get_story_file("tape-measure")
                },
                {
                    "name": "igloo",
                    "type": "directory",
                    "challenges": [
                        {
                            "challenge": 0,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 20,
                            "step": 5
                        }
                    ]
                }
            ]
        }
    ]
}
