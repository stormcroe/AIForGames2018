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


def on_mouse_release(x, y, button, modifiers):
    # print (x, y, button)
    if button == 1:  # left
        #print (x,y)
        world.target = Vector2D(x, y)


def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol == KEY.Q: #26/3/18
        win.has_exit = True
    elif symbol == KEY.RETURN: #26/3/18
        world.showinfo = not world.showinfo
    elif symbol == KEY.R: # 01/04/18
        # Reset to Default Values on limits, Randomise the Path of each agent
        for agent in world.agents:
            agent.reinit()
    elif symbol == KEY.L: # 09/04/18
        # Toggle Path Looping on all agents
        for agent in world.agents: 
            agent.path_looped = not agent.path_looped
            agent.randomise_path(agent.path_looped)
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
            #agent.reinit()

    # Neighbourhood Behaviour Modifiers
    #   Updated on 16/04/2018
    # On the Right and Left Brackets
    # Increase and Decrease Cohesion
    # Increase and Decrease Seperation with ctrl modifier
    # Increase and Decrease Alignment with alt modifier
    # Increase and Decrease The Radius to Tag Neighbours with shift modifier
    elif symbol == KEY.BRACKETLEFT:
        if (modifiers & KEY.MOD_CTRL):
            if world.seperation >= 0.10:
                world.seperation -= 0.10
        elif modifiers & KEY.MOD_ALT:
            if world.alignment >= 0.10:
                world.alignment -= 0.10
        elif modifiers & KEY.MOD_SHIFT:
            if world.radius >= 10:
                world.radius -= 10
        else:
            if world.cohesion >= 0.10:
                world.cohesion -= 0.10
    elif symbol == KEY.BRACKETRIGHT:
        if (modifiers & KEY.MOD_CTRL):
            world.seperation += 0.10
        elif modifiers & KEY.MOD_ALT:
            world.alignment += 0.10
        elif modifiers & KEY.MOD_SHIFT:
            world.radius += 10
        else:
            world.cohesion += 0.10
   

    # Use NUM_ADD and NUM_SUBTRACT to add or remove agents 
    elif symbol == KEY.NUM_ADD or symbol == KEY.PLUS: #26/3/18
        world.agents.append(Agent(world))
    elif (symbol == KEY.MINUS or symbol == KEY.NUM_SUBTRACT) and len(world.agents) != 0: #26/3/18
        world.agents.pop()

    # use NUM_MULTIPLY and NUM_DIVIDE to add to or subtract from every agents mass
    elif (symbol == KEY.NUM_MULTIPLY): #26/3/18
        for agent in world.agents:
            agent.mass += 1
    elif (symbol == KEY.NUM_DIVIDE): #26/3/18
        for agent in world.agents:
            agent.mass -= 1
            if agent.mass <= 0:
                agent.mass = 0.1

    # use UP and DOWN to adjust the MAX SPEED of All agents
    elif (symbol == KEY.UP): #26/3/18
        for agent in world.agents:
            agent.max_speed += 50
    elif (symbol == KEY.DOWN): #26/3/18
        for agent in world.agents:
            agent.max_speed -= 50
            if agent.max_speed < 0:
                agent.max_speed = 0




def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy


if __name__ == '__main__':

    # create a pyglet window and set glOptions
    win = window.Window(width=500, height=500, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_release)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(500, 500)
    # add one agent
    world.agents.append(Agent(world))
    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_display.draw()
        # swap the double buffer
        win.flip()

