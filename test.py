#!/usr/bin/env python3

from experiments import *
from railroad.geometry import *


def arc_center(p0, d0, p1, d1):
    pass


def update(x, y):
    mouse = coords_to_pos(x, y)

    draw.clear()

    s = Vec(-550, 0)
    b = Vec(-200, 50)
    e = Vec(550, -150)

    draw.pt(s, color=colors.blue)
    draw.pt(b, color=colors.blue)
    draw.pt(e, color=colors.blue)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    update(x, y)

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    update(x, y)


run()
