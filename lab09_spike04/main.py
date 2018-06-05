'''Autonomous Agent Movement: Seek, Arrive and Flee

Created for COS30002 AI for Games, Lab 05
By Clinton Woodward cwoodward@swin.edu.au

'''
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  # Agent with seek, arrive, flee and pursuit
from target import Target, AGENT_MODES 
from weapon import Weapon
from random import randrange


def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        world.target = Vector2D(x, y)


def on_key_press(symbol, modifiers):
    
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
    elif symbol ==KEY.T:
        world.prey[0].looped = True
        world.prey[0].move = True
        world.prey[0].randomise_path()
    elif symbol ==KEY.Y:
        world.prey[0].move = False
        world.prey[0].vel = Vector2D(0,0)
    elif symbol == KEY.S:
        if world.prey[0].hit is False:
            world.bullets.append(Weapon(world,world.bull_type))
    elif symbol == KEY.D:
        world.agents[0].pos.y = randrange(0.00, 800.00)
    elif symbol == KEY.G:
        if world.auto_fire is False:
            world.auto_fire = True
        else:
            world.auto_fire = False
    elif symbol == KEY.Q:
        world.bull_type = 'InAccuSlow'
    elif symbol == KEY.W:
        world.bull_type = 'InAccuFast'
    elif symbol == KEY.E:
        world.bull_type = 'AccuFast'
    elif symbol == KEY.R:
        world.bull_type = 'AccuSlow'
    elif symbol == KEY.H:
        world.bullets.clear()



def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy


if __name__ == '__main__':
    
    # create a pyglet window and set glOptions
    win = window.Window(width=1000, height=1000, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(500, 500)
    # add one agent
    world.agents.append(Agent(world))
    world.prey.append(Target(world))
    # unpause the world ready for movement
    world.paused = False
    i = 0
    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_display.draw()
        egi.text_at_pos(0, 95, "Bullet Type:")
        egi.text_at_pos(80, 95,str(world.bull_type)) 
        for bull in world.bullets:
            if bull.tagged is True:
                world.bullets.remove(bull)
            elif bull.pos.x >= 900.00 or bull.pos.y >= 900.00:
                world.bullets.remove(bull)
        if world.auto_fire is True and world.prey[0].hit is False:
            world.bullets.append(Weapon(world,world.bull_type))
        for t in world.prey:
            if i < 100:
                i+=1
            else:
                t.hit = False
                i = 0
        # swap the double buffer
        win.flip()

