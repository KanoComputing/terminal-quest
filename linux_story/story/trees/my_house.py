from linux_story.common import get_story_file
from garden import garden
from kitchen import kitchen
from my_room import my_room
from parents_room import parents_room

my_house = {
    "name": "my-house",
    "children": [
        my_room, kitchen, parents_room, garden
    ]
}
