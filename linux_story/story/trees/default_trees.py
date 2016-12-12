from farm import farm
from linux_story.common import get_story_file
from my_house import my_house
from woods import woods
from town import town

# duplicates from FileTree
TYPE_DIR = "directory"
TYPE_FILE = "file"


basket = {
    "name": "basket",
    "challenges": [
        {
            "challenge": 1,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 13,
            "step": 2
        },
        {
            "challenge": 13,
            "step": 5,
            "exists": False
        },
        {
            "challenge": 14,
            "step": 4
        },
        {
            "challenge": 14,
            "step": 5,
            "exists": False
        }
    ],
    "children": [
        {
            "name": "banana",
            "contents": get_story_file("banana"),
            "challenges": [
                {
                    "challenge": 14,
                    "step": 4
                }
            ]
        },
        {
            "name": "cake",
            "contents": get_story_file("cake"),
            "challenges": [
                {
                    "challenge": 14,
                    "step": 4
                }
            ]
        },
        {
            "name": "croissant",
            "contents": get_story_file("croissant"),
            "challenges": [
                {
                    "challenge": 14,
                    "step": 4
                }
            ]
        }
    ]
}


tree = {
    "name": "~",
    "children": [
        my_house,
        town,
        woods,
        farm,
        basket
    ]
}




