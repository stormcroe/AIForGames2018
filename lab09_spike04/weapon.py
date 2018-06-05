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

class Weapon(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal':0.5,
        'fast': 0.2
        ### ADD 'normal' and 'fast' speeds here
    }

    BULLET_TYPE = {
        'AccuFast': 8,
        'InAccuFast':3,
        'AccuSlow': 8,
        'InAccuSlow': 3
    ### With this enum the higher the number the more accurate
    }


    def __init__(self, world=None, gun_type = None, scale=30.0, mass=0.5):
        # keep a reference to the world object
        self.world = world
        self.tagged = False
        self.target_pos = None
        self.gun_type = gun_type
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(self.world.agents[0].pos.x,self.world.agents[0].pos.y)
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.acceleration = Vector2D()  # current steering force
        self.mass = mass
        self.radius = 35.00
        # limits?
        # data for drawing this agent
        self.color = 'WHITE'
        self.vehicle_shape = [
            Point2D(-0.2,  0.1),
            Point2D( 0.2,  0.0),
            Point2D(-.2, -0.1)
        ]

        self.moving_speed = 'slow'

        # limits?
        self.max_speed = 100.0 * scale
        self.max_force = 500.0
        self.turnRate = 3

    def calculate(self):
        # reset the steering force
        force = self.coll_check(self.world.prey[0])
        self.force = force
        return force

    def update(self, delta):
        ''' update Bullet position and orientation '''
        force = self.calculate()
        # new velocity
        if self.gun_type is 'AccuSlow' or self.gun_type is 'InAccuSlow':
            self.vel += force * (delta/4)
        if self.gun_type is 'AccuFast' or self.gun_type is 'InAccuFast':
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
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                        self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)



    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def coll_check(self, target):
        #check to see if you are within a certain distance of the target
        toTarget = target.pos - self.pos
        self.heading.dot(target.heading)
        if self.target_pos is not None:
            toTarget = self.target_pos - self.pos
            test = target.pos - self.pos
            if test.length() < self.radius:
                    target.hit = True
            if toTarget.length() < self.radius or target.hit is True:
                self.tagged = True
                return Vector2D(0,0)

        if target.vel == Vector2D(0,0) and self.target_pos is None:
            if randrange(1,10) <= self.BULLET_TYPE[self.gun_type]:
                self.target_pos = target.pos
            else:
                if randrange(1,10) <= 5:
                    self.target_pos = Vector2D(target.pos.x +100.0,target.pos.y +100.0)
                else:
                    self.target_pos = Vector2D(target.pos.x -100.0,target.pos.y -100.0)
            return self.seek(self.target_pos)
        if target.vel != Vector2D(0,0) and self.target_pos is None:
            if randrange(1,10) <= self.BULLET_TYPE[self.gun_type]:
                self.target_pos = (target.pos + target.vel) - self.vel.normalise()
                
            else:
                if randrange(1,10) <= 5:
                    self.target_pos = ((target.pos + target.vel) - self.vel.normalise()) + Vector2D(target.pos.x +50.0,target.pos.y +50.0)
                else:
                    self.target_pos = ((target.pos + target.vel) - self.vel.normalise()) + Vector2D(target.pos.x -50.0,target.pos.y -50.0)
            return self.seek(self.target_pos)
        return self.seek(self.target_pos)