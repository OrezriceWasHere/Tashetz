import math

def average(integers):
    return sum(integers) / len(integers)


def distance(p1, p2):
    # p1 and p2 are both dictionaries containing x key and y key
    return math.sqrt(((p2['x'] - p1['x']) ** 2) + ((p2['y'] - p1['y']) ** 2))


def middlePoint(p1, p2):
    # p1 and p2 are both dictionaries containing x key and y key
    return {'x': (p1['x'] + p2['x']) / 2,
            'y': (p1['y'] + p2['y']) / 2}


def maxi(a, b):
    return a if a > b else b

def mini(a, b):
     return a if a < b else b