from linux_story.common import get_story_file
from chest import chest


cage = {
    "name": "cage",
    "challenges": [
        {
            "challenge": 44,
            "step": 5,
            "permissions": 0500
        },
        {
            "challenge": 45,
            "step": 6,
            "permissions": 0755
        }
    ],
    "children": [
        {
            "name": "Edith",
            "contents": get_story_file("Edith")
        },
        {
            "name": "Edward",
            "contents": get_story_file("Edward")
        },
        {
            "name": "dog",
            "contents": get_story_file("dog")
        },
        {
            "name": "swordmaster",
            "contents": get_story_file("swordmaster-without-sword")
        },
        {
            "name": "Dad",
            "contents": get_story_file("Dad")
        },
        {
            "name": "Mum",
            "contents": get_story_file("Mum")
        },
        {
            "name": "grumpy-man",
            "contents": get_story_file("grumpy-man")
        },
        {
            "name": "Mayor",
            "contents": get_story_file("Mayor")
        }
    ]
}

rabbithole = {
    "name": "rabbithole",
    "type": "directory",
    "children": [
        cage,
        chest,
        {
            "name": "Rabbit",
            "contents": get_story_file("Rabbit")
        },
        {
            "name": "bell",
            "contents": get_story_file("bell")
        }
    ],
    "challenges": [
        {
            "challenge": 40,
            "step": 1,
            "permissions": 0755
        },
        {
            "challenge": 41,
            "step": 1,
            "permissions": 0000
        },
        {
            "challenge": 44,
            "step": 5,
            "permissions": 0755
        }
    ]
}