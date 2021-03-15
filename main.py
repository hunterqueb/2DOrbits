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


orbitingBodyR = 2 * [None]
orbitingBodyV = 2 * [None]

DU = 100
#  696,340km = 100 pixels
# mu = 1.32712440018*(10^11)
# TU = 1595.059 sec

# 0.393 pixels^3/s^2
mu = 0.39304

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
    x=originLocation[0], y=originLocation[1], radius=DU, color=STAR_COLOR, batch=mainBody)

# # # # # GENERATE ORBITING BODY # # # # #
# initialize the body
orbitBodyShape = shapes.Circle(
    x=0, y=0, radius=20, color=BLACK, batch=mainBody)


def updateOrbitBody(dt):
    delTime = 1/120
    global orbitingBodyR
    global orbitingBodyV
    rdot = 2 * [None]
    r = 2 * [None]
    if (not started):
        return
    rddot = calcAcceleration(orbitingBodyR)
    print(rddot)
    rdot[0] = (rddot[0] * delTime) + orbitingBodyV[0]
    rdot[1] = (rddot[1] * delTime) + orbitingBodyV[1]
    r[0] = (rdot[0] * delTime) + orbitingBodyR[0]
    r[1] = (rdot[0] * delTime) + orbitingBodyR[0]

    orbitingBodyV[0] = rdot[0]
    orbitingBodyV[1] = rdot[1]

    orbitingBodyR[0] = r[0]
    orbitingBodyR[1] = r[1]

    orbitBodyShape.x = orbitingBodyR[0] * DU + originLocation[0]
    orbitBodyShape.y = orbitingBodyR[1] * DU + originLocation[1]

    # this is where we integrate


def calcAcceleration(r):
    rddot = 2 * [None]
    normR = normVect(r)
    rddot[0] = -mu * r[0]/(normR*normR*normR)
    rddot[1] = -mu * r[1]/(normR*normR*normR)
    return rddot


@window.event
def on_draw():
    window.clear()
    stars.draw()
    mainBodyShape.draw()
    orbitBodyShape.draw()
    if orbitingBodyV[0] != None:
        pyglet.clock.schedule_interval(updateOrbitBody, 1/120)


@window.event
def on_mouse_press(x, y, button, modifiers):
    print("on press")
    print(x)
    print(y)
    print("")

    global pressLocX
    global pressLocY
    global orbitingBodyR
    global orbitingBodyV
    if orbitingBodyR[0] == None:
        orbitingBodyR[0] = (x - originLocation[0])/DU
        orbitingBodyR[1] = (y - originLocation[1])/DU
        orbitBodyShape.x = x
        orbitBodyShape.y = y
        orbitBodyShape.color = BLUE
        pressLocX = x
        pressLocY = y

    else:
        pass


@window.event
def on_mouse_release(x, y, button, modifiers):
    global pressLocX
    global pressLocY
    global started
    global orbitingBodyR
    global orbitingBodyV
    print("on release")
    print(x)
    print(y)
    print("")

    if orbitingBodyV[0] == None:
        orbitingBodyV[0] = (pressLocX - x)/DU
        orbitingBodyV[1] = (pressLocY - y)/DU

        # print(orbitingBodyV)
        started = True
    pass


# @window.event
# def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
#     pass


pyglet.app.run()
