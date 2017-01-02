from linux_story.common import get_story_file

house = {
    "name": "house",
    "children": [
        {
           "name": "swordmaster",
            "contents": get_story_file("swordmaster")
        },
        {
            "name": "note",
            "contents": get_story_file("note_woods"),
            "challenges": [
                {
                    "challenge": 1,
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
            "challenge": 1,
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
            "challenge": 1,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 32,
            "step": 1
        }
    ]
}