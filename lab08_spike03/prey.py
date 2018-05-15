'''An Agent that has specifically flees another agent
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

class Prey(Agent):

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='wander', looped = True):
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
        # Random Path to follow in PathFollow mode
        self.path = Path()
        self.path_looped = looped
        self.randomise_path(looped)
        self.waypoint_threshold = 20
        # Wander Info
        self.wander_target = Vector2D (1,0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 1.0 * scale
        self.bRadius = scale

        #for hide behaviour
        self.BestHidingSpot = None

        # If Tagged is true, We are part of a neighbourhood
        self.tagged = False

        # data for drawing this agent
        self.color = 'GREEN'
        self.vehicle_shape = [
            Point2D(-1.0,  0.7),
            Point2D( 1.1,  0.0),
            Point2D(-1.0, -0.5)
        ]

    def calculate(self, delta):
        if self.mode == 'flee':
            force = self.runAway(self.world.hunter, delta)
        elif self.mode == 'hide':
            force = self.hide(self.world.hunter, self.world.hideObjects, delta)
        else:
            force = super().calculate(delta)
        return force

    def runAway(self, pursuer, delta):
        # flee from the estimated future position
        toPursuer = pursuer.pos - self.pos
        if (toPursuer.length() - pursuer.radius)< -50:
            # proportional to distance, inversely proportional to sum of velocities
            lookAheadTime = toPursuer.length() / (self.max_speed
            + pursuer.speed())
            # go in the opposite predicted position
        
            return self.flee(pursuer.pos, 'fast',(pursuer.vel * lookAheadTime))        

        return self.wander(delta)

    def flee(self, hunter_pos, speed, pursuit_speed):
        ''' move away from hunter position '''

        decel_rate = self.DECELERATION_SPEEDS[speed]
        flee_target = self.pos - hunter_pos
        dist = flee_target.length()
        if dist > 100:
            if AGENT_MODES is 'flee': ## For stationary targets
                speed = dist / decel_rate
                speed = min(speed, self.max_speed)
                desired_vel = flee_target * (speed / dist)
                return (desired_vel - self.vel)
            else: ## for moving targets
                pursuit_speed = dist / decel_rate 
                pursuit_speed = min(pursuit_speed, self.max_speed)
                desired_vel = flee_target * (pursuit_speed / dist)
                return (desired_vel - self.vel)
        return Vector2D()

    def getHidingPosition(self, hunter, obj):
        # set the distance between the object and the hiding point
        DistFromBoundary = 30.0 # system setting
        DistAway = obj.radius + DistFromBoundary
        # get the normal vector from the hunter to the hiding point
        ToObj = Vector2D.get_normalised(obj.pos - hunter.pos)
        # scale size past the object to the hiding location
        return (ToObj*DistAway)+obj.pos 
        
    def hide(self,hunter,objs, delta):
        DistToClosest = 1000000
        
        self.BestHidingSpot = None
        hun = hunter
        # check for possible hiding spots
        for obj in objs:
            HidingSpot = self.getHidingPosition(hun,obj)
            HidingDist = Vector2D.distance_sq(HidingSpot,self.pos)
            # render the hiding spots immediatly
            egi.aqua_pen()
            egi.cross(HidingSpot, 5)

            if HidingDist < DistToClosest and (Vector2D.length(hun.pos - obj.pos) - hun.radius) > 0:
                DistToClosest = HidingDist
                self.BestHidingSpot = HidingSpot
        # if we have a best hiding spot, use it

        if self.BestHidingSpot is not None:
            return self.arrive(self.BestHidingSpot, 'fast') # speed = fast?
        # default - run away!
        return self.runAway(hunter, delta) 