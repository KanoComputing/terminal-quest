
from cave import cave
from clearing import clearing

woods = {
    "name": "woods",
    "challenges": [
        {
            "challenge": 1,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 32,
            "step": 1
        }
    ],
    "children": [
        clearing,
        cave
    ]
}