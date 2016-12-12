from linux_story.common import get_story_file

shelves = {
    "name": "shelves",
    "children":
        [
            {
                "name": "redwall",
                "contents": get_story_file("redwall")
            },
            {
                "name": "watership-down",
                "contents": get_story_file("watership-down")
            },
            {
                "name": "alice-in-wonderland",
                "contents": get_story_file("alice-in-wonderland")
            },
            {
                "name": "comic-book",
                "contents": get_story_file("comic-book")
            },
            {
                "name": "note",
                "contents": get_story_file("note_my-room")
            }
        ]
}

wardrobe = {
    "name": "wardrobe",
    "children": [
        {
            "name": "cap",
            "contents": get_story_file("cap")
        },
        {
            "name": "dress",
            "contents": get_story_file("dress")
        },
        {
            "name": "jumper",
            "contents": get_story_file("jumper")
        },
        {
            "name": "shirt",
            "contents": get_story_file("shirt")
        },
        {
            "name": "skirt",
            "contents": get_story_file("skirt")
        },
        {
            "name": "t-shirt",
            "contents": get_story_file("t-shirt")
        },
        {
            "name": "trousers",
            "contents": get_story_file("trousers")
        }
    ]
}

chest = {
    "name": ".chest",
    "challenges": [
        {
            "challenge": 15,
            "step": 1
        }
    ],
    "children": [
        {
            "name": "CAT",
            "contents": get_story_file("CAT")
        },
        {
            "name": "CD",
            "contents": get_story_file("CD")
        },
        {
            "name": "LS",
            "contents": get_story_file("LS")
        },
        {
            "name": ".note",
            "contents": get_story_file(".note")
        }
    ]
}

my_room = {
    "name": "my-room",
    "children": [
        {
            "name": "alarm",
            "contents": get_story_file("alarm")
        },
        {
            "name": "chair",
            "contents": get_story_file("chair")
        },
        {
            "name": "computer",
            "contents": get_story_file("computer")
        },
        {
            "name": "desk",
            "contents": get_story_file("desk")
        },
        {
            "name": "bed",
            "contents": get_story_file("bed_my-room")
        },
        shelves,
        wardrobe,
        chest
    ]
}