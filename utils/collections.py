def map_items(items):
    map = {}
    for item in items:
        id = map.get(item)
        if id is None:
            map[item] = 1
        else:
            map[item] += 1
    return map
