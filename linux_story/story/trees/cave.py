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
            "challenge": 33,
            "step": 8,
            "permissions": 0700
        }
    ],
    "children": [
        {
            "name": "instructions",
            "contents": get_story_file("instructions-dark-room")
        }
    ]
}

cage_room = {
    "name": "cage-room",
    "challenges": [
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0500
        },
        {
            "challenge": 33,
            "step": 15,
            "permissions": 0700
        }
    ],
    "children": [
        {
            "name": "bird",
            "contents": get_story_file("bird"),
            "challenges": [
                {
                    "challenge": 33,
                    "step": 17,
                    "exists": False
                }
            ]
        },
        {
            "name": "lighter",
            "contents": get_story_file("lighter")
        },
        {
            "name": "w-sign",
            "contents": get_story_file("w-sign")
        },
        {
            "name": "x-scroll",
            "contents": get_story_file("x-scroll"),
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 33,
                    "step": 17
                }
            ]
        }
    ]
}

doorless_room = {
    "name": "doorless-room",
    "challenges": [
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0600
        },
        {
            "challenge": 35,
            "step": 20,
            "permissions": 0700
        }
    ],
    "children": [
        {
            "name": "firework-animation",
            "contents": get_story_file("firework-animation")
        }
    ]
}

chest = {
    "name": "chest",
    "permissions": 0000,
    "children": [
        {
            "name": "riddle",
            "contents": get_story_file("riddle-cave")
        },
        {
            "name": "answer",
            "contents": get_story_file("answer-cave")
        }
    ]
}

cave = {
    "name": "cave",
    "children": [
        {
            "name": "sign",
            "contents": get_story_file("sign_cave")
        },
        {
            "name": "r-sign",
            "contents": get_story_file("r-sign")
        },
        dark_room,
        cage_room,
        doorless_room,
        chest
    ]
}