import string
import random


def randomString(stringLength=10):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))
