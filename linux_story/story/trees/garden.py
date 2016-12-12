from linux_story.common import get_story_file

greenhouse = {
    "name": "greenhouse",
    "children": [
        {
            "name": "carrots",
            "contents": get_story_file("carrots")
        },
        {
            "name": "pumpkin",
            "contents": get_story_file("pumpkin")
        },
        {
            "name": "tomato",
            "contents": get_story_file("tomato")
        },
        {
            "name": "onion",
            "contents": get_story_file("onion")
        },
        {
            "name": "Dad",
            "contents": get_story_file("Dad"),
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1
                },
                {
                    "challenge": 4,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "note",
            "contents": get_story_file("note_greenhouse"),
            "challenges":
                [
                    {
                        "challenge": 4,
                        "step": 3
                    }
                ]
        }
    ]
}
garden = {
    "name": "garden",
    "children": [
        {
            "name": "bench",
            "contents": get_story_file("bench")
        },
        {
            "name": "flowers",
            "contents": get_story_file("flowers")
        },
        {
            "name": "fence",
            "contents": get_story_file("fence")
        },
        greenhouse
    ]
}