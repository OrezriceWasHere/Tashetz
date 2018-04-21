from __future__ import division
import Mathematics
from Mathematics import *

class Linearline:

    NO_INTERSECTION = -1

    def __init__(self, deltaY, deltaX, x0, y0):
        self.derrative = deltaY / deltaX
        self.x0 = x0
        self.y0 = y0
        pass

    def y(self, x):
        return int(math.floor(self.derrative * (x - self.x0) + self.y0))

    def x(self, y):
        return int(math.floor(((y - self.y0) / self.derrative) + self.x0))



    def intersectWithSection(self, p1, p2):
        # This function checks whether the line(self) intersects with a "section",
        # a line limited by the two points given.
        # it returns the distance between line's x0, y0 point to intersection point (or -1 if no intersection)

        if p2['x'] == p1['x']:
            #  p2 and p1 are parallel to x axis
            intersection_point = {"x": p1['x'], "y": self.y(p1['x'])}

        else:
            other_line = Linearline(p2['y'] - p1['y'],
                                    p2['x'] - p1['x'],
                                    p2['x'],
                                    p2['y'])

            if other_line.derrative == self.derrative:
                return Linearline.NO_INTERSECTION

            x_intersection = (other_line.y(0) - self.y(0)) / (self.derrative - other_line.derrative)
            intersection_point = {"x": x_intersection, "y": self.y(x_intersection)}



        if intersection_point['y'] > Mathematics.maxi(p1['y'], p2['y']) or \
           intersection_point['y'] < Mathematics.mini(p1['y'], p2['y']) or \
                intersection_point['x'] > Mathematics.maxi(p1['x'], p2['x']) or \
                intersection_point['x'] < Mathematics.mini(p1['x'], p2['x']):

            return Linearline.NO_INTERSECTION

        return Mathematics.distance(intersection_point, {"x": self.x0, "y": self.y0})