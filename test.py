#!/usr/bin/env python3

from experiments import *

def update(x, y):
    mouse = coords_to_pos(x, y)

    draw.clear()

    origin = Vec(-200, -150)
    vector = mouse - origin

    draw.vec(origin, vector, 100, color=colors.grey)
    draw.vec(origin, vector.rotated(45), 100, colors.green)
    draw.vec(origin, vector.rotated(-45), 100, colors.red)
    draw.vec(origin, vector.rotated(60), 100, colors.blue)
    draw.vec(origin, vector.rotated(120), 100, colors.blue)
    draw.vec(origin, vector.rotated(180), 100, colors.blue)
    draw.vec(origin, vector.rotated(240), 100, colors.blue)
    draw.vec(origin, vector.rotated(300), 100, colors.blue)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    update(x, y)

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    update(x, y)


run()
