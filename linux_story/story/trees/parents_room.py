from linux_story.common import get_story_file

safe = {
    "name": ".safe",
    "challenges": [
        {
            "challenge": 17,
            "step": 1
        }
    ],
    "children": [
        {
            "name": "mums-diary",
            "contents": get_story_file("mums-diary"),
        },
        {
            "name": "ECHO",
            "contents": get_story_file("ECHO"),
        },
        {
            "name": "map",
            "contents": get_story_file("map"),
        }
    ]
}

parents_room = {
    "name": "parents-room",
    "children": [
        {
            "name": "picture",
            "contents": get_story_file("picture")
        },
        {
            "name": "tv",
            "contents": get_story_file("tv")
        },
        {
            "name": "window",
            "contents": get_story_file("window")
        },
        {
            "name": "bed",
            "contents": get_story_file("bed_parents-room")
        },
        safe
    ]
}