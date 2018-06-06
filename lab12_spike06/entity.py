from graphics import egi
from math import sqrt
from point2d import Point2D


class Entity(object): 
### This is the entity that follows the path returned by the algorithms
    def __init__(self, x, y, boxes):
        self.pos = Point2D(x, y)
        self.path = []
        self.radius = 10
        self.speed = 1
        self.boxes = boxes
        self.end = False
    def draw(self):
        egi.black_pen()
        egi.circle(self.pos,20,False)

    def update(self):
        if len(self.path) > 0:
            # update position and progress
            src = self.pos
            dest = self.boxes[self.path[0]]._vc
            scale = 0.9
            self.pos.x = (src.x + (dest.x - src.x) * scale)
            self.pos.y = (src.y + (dest.y - src.y) * scale)
            if self.pos.x == dest.x and self.pos.y == dest.y:
                self.path = self.path[1:]
            if len(self.path) is 0:
                self.end = True