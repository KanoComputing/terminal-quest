from linux_story.common import get_story_file

kitchen = {
    "name": "kitchen",
    "children": [
        {
            "name": "basket",
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 13,
                    "step": 5
                },
                {
                    "challenge": 14,
                    "step": 4,
                    "exists": False
                }
            ],
            "children": [
                {
                    "name": "empty-bottle",
                    "contents": get_story_file("empty-bottle")
                }
            ]
        },
        {
            "name": "banana",
            "contents": get_story_file("banana"),
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1
                },
                {
                    "challenge": 14,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "cake",
            "contents": get_story_file("cake"),
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1,
                },
                {
                    "challenge": 14,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "croissant",
            "contents": get_story_file("croissant"),
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1
                },
                {
                    "challenge": 14,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "grapes",
            "contents": get_story_file("grapes")
        },
        {
            "name": "milk",
            "contents": get_story_file("milk")
        },
        {
            "name": "pie",
            "contents": get_story_file("pie")
        },
        {
            "name": "sandwich",
            "contents": get_story_file("sandwich")
        },
        {
            "name": "newspaper",
            "contents": get_story_file("newspaper")
        },
        {
            "name": "oven",
            "contents": get_story_file("oven")
        },
        {
            "name": "table",
            "contents": get_story_file("table")
        },
        {
            "name": "note",
            "contents": get_story_file("note_kitchen"),
            "challenges": [
                {
                    "challenge": 8,
                    "step": 1
                },
                {
                    "challenge": 10,
                    "step": 1
                }
            ]
        },
        {
            "name": "Mum",
            "contents": get_story_file("Mum"),
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1
                },
                {
                    "challenge": 8,
                    "step": 1,
                    "exists": False
                }
            ]
        }

    ]
}