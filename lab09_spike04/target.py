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


class Target(object):

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
        self.looped = False
        self.move = False
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.acceleration = Vector2D()  # current steering force
        self.mass = mass
        self.hit = False
        self.hit_color = 'RED'
        # limits?
        # data for drawing this agent
        self.color = 'GREEN'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        
        self.path = Path()
        self.randomise_path()
        self.waypoint_threshold = 300.0
        
        self.moving_speed = 'slow'

        # limits?
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        ## max_force ??

        # debug draw info?
        self.show_info = False

    def calculate(self, delta):
        # reset the steering force
        mode = self.mode
        if mode == 'shoot' and self.move:
            force = self.follow_path()
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        force = self.calculate(delta)
        if self.hit is True:
            self.color = self.hit_color
            force *= 0.5
        else:
            self.color = 'GREEN' 
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

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)


    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)
    
    def randomise_path(self):
        cx = self.world.cx
        cy = self.world.cy
        margin = min(cx,cy) * (1/6)
        self.path.create_random_path(2, 0+margin,0+margin, self.world.cx - margin, self.world.cy - margin, self.looped)

    def follow_path(self):
        if (self.path.is_finished()) :
            return self.arrive(self.world.target, self.moving_speed)
        else:
            dist = self.path.current_pt() - self.pos
            if dist.length() < self.waypoint_threshold:
                self.path.inc_current_pt()
            return self.seek(self.path.current_pt())
