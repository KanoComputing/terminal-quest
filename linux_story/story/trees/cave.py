from linux_story.common import get_story_file

dark_room = {
    "name": "dark-room",
    "permissions": 0300,
    "children": [
        {
            "name": "instructions",
            "contents": get_story_file("instructions-dark-room")
        }
    ]
}

cage_room = {
    "name": "cage-room",
    "permissions": 0500,
    "children": [
        {
            "name": "bird",
            "contents": get_story_file("bird")
        }
    ]
}

doorless_room = {
    "name": "doorless-room",
    "permissions": 0600,
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
            "name": "sign-1",
            "contents": get_story_file("sign_cave")
        },
        {
            "name": "sign-2",
            "contents": get_story_file("sign-cave-2")
        },
        dark_room,
        cage_room,
        doorless_room,
        chest
    ]
}