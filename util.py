import random

def random_color():
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)