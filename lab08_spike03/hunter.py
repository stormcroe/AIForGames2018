'''An Agent that has specifically seeks another agent
    Author: Peter Argent
    Created 2018-05-07
'''

from agent import *
from path import Path
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform

class Hunter(Agent):

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='pursuit', looped = True):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.acceleration = Vector2D()  # current steering force
        self.mass = mass
        # limits?
        self.max_speed = 20.0 * scale / 2
        self.max_force = 500.0
        
        # Wander Info
        self.wander_target = Vector2D (1,0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 1.0 * scale
        self.bRadius = scale

        #Pursuit Info
        self.radius = self.world.radius + 10

        # If Tagged is true, We are part of a neighbourhood
        self.tagged = False

        # data for drawing this agent
        self.show_info = False
        self.color = 'RED'
        self.vehicle_shape = [
            Point2D(-1.0,  0.7),
            Point2D( 1.1,  0.0),
            Point2D(-1.0, -0.5)
        ]
    
    def calculate(self, delta):
        if self.mode == "pursuit":
            force = self.pursuit(self.world.agents, delta)
            force.truncate(self.max_force)
            accel = Vector2D(force.x / self.mass, force.y / self.mass)
            self.acceleration = accel
            return accel
        else:
            return super().calculate(delta)
        return super().calculate(delta)
    
    def pursuit(self, evader, delta):
        ''' this behaviour predicts where an agent will be in time T and seeks
        towards that point to intercept it. '''
        for ev in evader:
            # assumes that evader is a Vehicle
            toEvader = ev.pos - self.pos
            relativeHeading = self.heading.dot(ev.heading)
            # simple out: if target is ahead and facing us, head straight to it
            if ((toEvader.length() - self.radius) < 0):
                if toEvader.length() < 50:
                    ev.tagged = True
                return self.seek(ev.pos)        
        return self.wander(delta)

    def wander(self, delta):
        return super().wander(delta)

    def render(self, color = None):
        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.acceleration * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.acceleration+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.acceleration+self.vel) * s, 5)

        return super().render(color)

    def update(self, delta):
        return super().update(delta)

