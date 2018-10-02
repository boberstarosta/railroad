#!/usr/bin/env python3

from experiments import *
from railroad.geometry import *


def arc_center(p0, d0, p1, d1):
    pass


def update(x, y):
    mouse = coords_to_pos(x, y)

    draw.clear()

    g = Vec(-550, 90)
    s = Vec(-450, 100)
    e = Vec(300, -150)
    f = Vec(400, -250)

    draw.pt(g, color=colors.blue)
    draw.pt(s, color=colors.blue)
    draw.pt(e, color=colors.blue)
    draw.pt(f, color=colors.blue)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    update(x, y)

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    update(x, y)


run()
