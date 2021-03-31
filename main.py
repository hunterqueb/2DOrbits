import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import shapes
from pyglet import clock

from vectorMath import *
# import numpy as np
import random

# COLORS #

WHITE = (255, 255, 255)
STAR_COLOR = (216, 216, 0)
BLUE = (6, 37, 189)
BLACK = (0, 0, 0)


width = 1000
height = 1000

originLocation = [width//2, height//2]

window = pyglet.window.Window(width=width, height=height)

stars = pyglet.graphics.Batch()
mainBody = pyglet.graphics.Batch()
orbitingBody = pyglet.graphics.Batch()

r = 2 * [None]
v = 2 * [None]
orbitingBodyR = 2 * [None]
orbitingBodyV = 2 * [None]
accel1 = 2 * [None]
accel2 = 2 * [None]

DU = 100
#  696,340km = 100 pixels
# mu = 1.32712440018*(10^11)
# TU = 1595.059 sec

# 0.393 pixels^3/s^2
mu = 0.39304


G = 1/50
mass1 = 170000
mass2 = 58

pressLocX = 0
pressLocY = 0

started = False

# # # # # GENERATE STARS # # # # #

numStars = random.randint(45, 100)
starVector = numStars * [None]

for i in range(numStars):
    starVector[i] = shapes.Circle(x=random.randint(5, width), y=random.randint(
        5, height), radius=5, color=WHITE, batch=stars)

# # # # # GENERATE MAIN BODY # # # # #

mainBodyShape = shapes.Circle(
    x=originLocation[0], y=originLocation[1], radius=78, color=STAR_COLOR, batch=mainBody)

# # # # # GENERATE ORBITING BODY # # # # #
# initialize the body
orbitBodyShape = shapes.Circle(
    x=0, y=0, radius=20, color=BLACK, batch=mainBody)


def updateOrbitBody(dt):
    Force = calcForce(r)

    accel1[0] = Force/mass1 * r[0]/normVect(r)
    accel1[1] = Force/mass1 * r[1]/normVect(r)

    accel2[0] = -Force/mass2 * r[0]/normVect(r)
    accel2[1] = -Force/mass2 * r[1]/normVect(r)

    orbitingBodyV[0] += (accel2[0] * dt)
    orbitingBodyV[1] += (accel2[1] * dt)

    orbitingBodyR[0] += (orbitingBodyV[0] * dt)
    orbitingBodyR[1] += (orbitingBodyV[1] * dt)

    orbitBodyShape.x = orbitingBodyR[0]
    orbitBodyShape.y = orbitingBodyR[1]

    r[0] = orbitingBodyR[0] - originLocation[0]
    r[1] = orbitingBodyR[1] - originLocation[1]

    # print(normVect(orbitingBodyV))
    pass
    # this is where we integrate


def calcForce(r):
    normR = normVect(r)
    return G * mass1 * mass2 / (normR * normR)
    


@window.event
def on_draw():
    window.clear()
    stars.draw()
    mainBodyShape.draw()
    orbitBodyShape.draw()
    if v[0] != None:
        pyglet.clock.schedule_interval(updateOrbitBody, 1/60)


@window.event
def on_mouse_press(x, y, button, modifiers):
    # print("on press")
    # print(x)
    # print(y)
    # print("")

    orbitingBodyR[0] = x
    orbitingBodyR[1] = y

    r[0] = orbitingBodyR[0] - originLocation[0]
    r[1] = orbitingBodyR[1] - originLocation[1]

    orbitBodyShape.x = x
    orbitBodyShape.y = y
    orbitBodyShape.color = BLUE



@window.event
def on_mouse_release(x, y, button, modifiers):

    # print("on release")
    # print(x)
    # print(y)
    # print("")

    orbitingBodyV[0] = (orbitingBodyR[0] - x)/50
    orbitingBodyV[1] = (orbitingBodyR[1] - y)/50

    v[0] = orbitingBodyV[0]
    v[1] = orbitingBodyV[1]


# @window.event
# def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
#     pass


pyglet.app.run()
