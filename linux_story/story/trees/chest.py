from linux_story.common import get_story_file

chest = {
    "name": "chest",
    "children": [
        {
            "name": "torn-scroll",
            "contents": get_story_file("torn-sudo"),
        },
        {
            "name": "torn-note",
            "contents": get_story_file("torn-note")
        }
    ],
    "challenges": [
        {
            "challenge": 1,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 44,
            "step": 5
        }
    ]
}