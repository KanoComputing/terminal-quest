from linux_story.common import get_story_file

library = {
    "name": "library",
    "children": [
        {
            "name": "private-section",
            "type": "directory",
            "challenges": [
                {
                    "challenge": 1,
                    "step": 1,
                    "permissions": 0000
                },
                {
                    "challenge": 43,
                    "step": 3,
                    "permissions": 0700
                }
            ],
            "children": [
                {
                    "name": "chest",
                    "challenges": [
                        {
                            "challenge": 1,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 43,
                            "step": 4
                        }
                    ],
                    "children": [
                        {
                            "name": "scroll",
                            "contents": get_story_file("SUDO"),
                        }
                    ]
                },
                {
                    "name": "torn-note",
                    "contents": get_story_file("torn-note"),
                    "challenges": [
                        {
                            "challenge": 1,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 43,
                            "step": 4
                        }
                    ],
                }
            ]
        },
        {
            "name": "public-section",
            "type": "directory"
        }
    ]
}