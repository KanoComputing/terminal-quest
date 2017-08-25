from linux_story.common import get_story_file


library = {
    "name": "library",
    "children": [
        {
            "name": "Rabbit",
            "type": "file",
            "contents": get_story_file("Rabbit"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 42,
                    "step": 1,
                },
                {
                    "challenge": 42,
                    "step": 4,
                    "exists": False
                }
            ]
        },
        {
            "name": "private-section",
            "type": "directory",
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "permissions": 0000
                },
                {
                    "challenge": 42,
                    "step": 3,
                    "permissions": 0755
                }
            ],
            "children": [
                {
                    "name": "chest",
                    "children": [
                        {
                            "name": "scroll",
                            "contents": get_story_file("scroll"),
                        },
                        {
                            "name": "torn-note",
                            "contents": get_story_file("torn-note")
                        }
                    ],
                    "challenges": [
                        {
                            "challenge": 0,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 42,
                            "step": 3
                        },
                        {
                            "challenge": 42,
                            "step": 6,
                            "exists": False
                        }
                    ]
                },
                {
                    "name": "Rabbit",
                    "type": "file",
                    "contents": get_story_file("Rabbit"),
                    "challenges": [
                        {
                            "challenge": 0,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 42,
                            "step": 4
                        },
                        {
                            "challenge": 42,
                            "step": 6,
                            "exists": False
                        }
                    ]
                },
                {
                    "name": "note",
                    "contents": get_story_file("note_private-section"),
                    "challenges": [
                        {
                            "challenge": 0,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 42,
                            "step": 7
                        },
                        {
                            "challenge": 43,
                            "step": 5
                        }
                    ]
                },
                {
                    "name": "sword",
                    "contents": get_story_file("RM-sword"),
                    "challenges": [
                        {
                            "challenge": 0,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 43,
                            "step": 2
                        }
                    ]
                }
            ]
        },
        {
            "name": "public-section",
            "children": [
                {
                    "name": "NANO",
                    "contents": get_story_file("NANO")
                }
            ]
        }
    ]
}