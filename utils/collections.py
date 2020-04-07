import string
import random


def map_items(items):
    map = {}
    for item in items:
        id = map.get(item)
        if id is None:
            map[item] = 1
        else:
            map[item] += 1
    return map


def randomString(stringLength=10):
    letters = string.ascii_lowercase.upper()
    return ''.join(random.choice(letters) for i in range(stringLength))
