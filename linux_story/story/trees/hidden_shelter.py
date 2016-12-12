from linux_story.common import get_story_file

eleanor_hidden_shelter = {
    "name": "Eleanor",
    "contents": get_story_file("Eleanor"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 11,
            "step": 6,
            "exists": False
        },
        {
            "challenge": 12,
            "step": 1
        },
        {
            "challenge": 23,
            "step": 4,
            "exists": False
        }
    ]
}

dog_hidden_shelter = {
    "name": "dog",
    "contents": get_story_file("dog"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 11,
            "step": 6,
            "exists": False
        },
        {
            "challenge": 22,
            "step": 2,
            "exists": False
        }
    ]
}


edith_hidden_shelter = {
    "name": "Edith",
    "contents": get_story_file("Edith"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 22,
            "step": 4,
            "exists": False
        }
    ]
}


edward_hidden_shelter = {
    "name": "Edward",
    "contents": get_story_file("Edward"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 22,
            "step": 4,
            "exists": False
        }
    ]
}


apple_hidden_shelter = {
    "name": "apple",
    "contents": get_story_file("apple"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 11,
            "step": 5,
            "exists": False
        },
        {
            "challenge": 11,
            "step": 6
        }
    ]
}


apple_basket = {
    "name": "apple",
    "contents": get_story_file("apple"),
    "challenges": [
        {
            "challenge": 11,
            "step": 5,
            "exists": False
        },
        {
            "challenge": 11,
            "step": 6
        }
    ]
}


basket_hidden_shelter = {
    "name": "basket",
    "type": "directory",
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 13,
            "step": 2,
            "exists": False
        },
        {
            "challenge": 14,
            "step": 6
        }
    ],
    "children": [
        apple_basket
    ]
}


tiny_chest = {
    "name": "MV",
    "contents": get_story_file("MV"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        }
    ]
}


hidden_shelter = {
    "name": ".hidden-shelter",
    "children": [
        basket_hidden_shelter,
        tiny_chest,
        apple_hidden_shelter,
        dog_hidden_shelter,
        edith_hidden_shelter,
        eleanor_hidden_shelter,
        edward_hidden_shelter
    ]
}
