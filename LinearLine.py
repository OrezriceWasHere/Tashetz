from __future__ import division
import math

class Linearline:


    def __init__(self, deltaY, deltaX, x0, y0):
        self.derrative = deltaY / deltaX
        self.x0 = x0
        self.y0 = y0
        pass

    def y(self, x):
        return int(math.floor(self.derrative * (x - self.x0) + self.y0))