from shed_shop import shed_shop
from library import library

east = {
    "name": "east",
    "children": [
        shed_shop,
        library
    ],
    "challenges": [
        {
            "challenge": 1,
            "step": 1,
            "exists": False
        }
    ]
}