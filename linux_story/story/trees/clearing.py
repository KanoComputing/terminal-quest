from linux_story.common import get_story_file

house = {
    "name": "house",
    "permissions": 0000,
    "children": [
        {
           "name": "swordmaster",
            "contents": get_story_file("swordmaster")
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
    ]
}