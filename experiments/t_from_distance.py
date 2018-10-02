#!/usr/bin/env python3

from experiments import *
from railroad.geometry import *


def update(x, y):
    mouse = coords_to_pos(x, y)

    draw.clear()
    start = Vec(-400, -300)
    end = Vec(0, 0)
    point = mouse
    params = t_from_distance(point, start, end - start, 300)
    solutions = [start + (end - start)*t for t in params]

    print(params)

    draw.line(Vec(280, -380), Vec(580, -380), color=colors.grey)

    draw.line(start, end, color=colors.grey)
    draw.pt(start, colors.green)
    draw.pt(end, colors.red)

    draw.pt(point, color=colors.blue)

    for s in solutions:
        draw.pt(s, color=colors.yellow)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    update(x, y)

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    update(x, y)


run()
