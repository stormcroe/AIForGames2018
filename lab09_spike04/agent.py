'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path
from tkinter import Scale


AGENT_MODES = {
    KEY._1: 'shoot'
}


class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal':0.5,
        'fast': 0.2
        ### ADD 'normal' and 'fast' speeds here
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='shoot'):
        # keep a reference to the world object
        self.world = world
        self.points = 1
        self.mode = mode
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(100.00, randrange(0.00, 600.00))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.acceleration = Vector2D()  # current steering force
        self.mass = mass
        # limits?
        # data for drawing this agent
        self.color = 'BLUE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]


        # limits?
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        ## max_force ??

        # debug draw info?
        self.show_info = False

    def calculate(self, delta):
        # reset the steering force
        mode = self.mode
        if mode == 'shoot':
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        force = self.calculate(delta)
        # new velocity
        self.vel += force * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            ## ...
            self.path.render()
            pass

        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                        self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)


        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)


    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

