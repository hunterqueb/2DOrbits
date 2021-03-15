import pyglet
from pyglet.window import key
from pyglet import shapes
import numpy as np
import random

width = 1000
height = 1000

window = pyglet.window.Window(width=width, height=height)

# # # # # GENERATE STARS # # # # #
stars = pyglet.graphics.Batch()

numStars = random.randint(45, 100)
starVector = numStars * [None]

for i in range(numStars):
    starVector[i] = shapes.Circle(x=random.randint(
        5, width), y=random.randint(5, height), radius=5, color=(255, 255, 255), batch=stars)





@window.event
def on_draw():
    window.clear()
    stars.draw()

pyglet.app.run()
