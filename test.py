#!/usr/bin/env python3

from experiments import *



def update(x, y):
    mouse = coords_to_pos(x, y)

    draw.clear()

    # do stuff

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    update(x, y)

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    update(x, y)


run()
