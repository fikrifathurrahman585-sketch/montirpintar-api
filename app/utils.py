from collections import Counter


def duplicate(items):

    counter = Counter(items)

    return [

        item

        for item, count in counter.items()

        if count > 1

    ]
