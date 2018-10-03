#!/usr/bin/env python3

from collections import namedtuple
from experiments import *
from railroad.geometry import intersect_param


class Rect(namedtuple("Rect", ("center", "size", "rotation"))):

    def __new__(cls, *args):
        if len(args) == 3:
            center = args[0]
            size = args[1]
            rotation = args[2]
        elif len(args) == 5:
            center = Vec(args[0], args[1])
            size = Vec(args[2], args[3])
            rotation = args[4]
        else:
            raise ValueError("Wrong arguments")
        return super().__new__(cls, center, size, rotation)

    @property
    def axis_x(self):
        return Vec.from_angle(self.rotation)

    @property
    def axis_y(self):
        return Vec.from_angle(self.rotation + 90)

    @property
    def corners(self):
        left = -self.axis_x * self.size.x/2
        right = self.axis_x * self.size.x/2
        bottom = -self.axis_y * self.size.y/2
        top = self.axis_y * self.size.y/2

        return[
            self.center + left + bottom,
            self.center + right + bottom,
            self.center + right + top,
            self.center + left + top
        ]

    @classmethod
    def intersect(cls, r0, r1):
        corners0 = r0.corners
        corners1 = r1.corners

        sides0 = []
        for i in range(len(corners0)):
            sides0.append((corners0[i], corners0[(i + 1)%len(corners0)]))
        sides1 = []
        for i in range(len(corners1)):
            sides1.append((corners1[i], corners1[(i + 1)%len(corners1)]))

        for p0, d0 in sides0:
            for p1, d1 in sides0:
                t = intersect_param(p0, d0, p1, d1)
                if 0 <= t <= 1:
                    return True

        return False


def draw_rect(rect, color):
    for i in range(len(rect.corners)):
        draw.line(rect.corners[i], rect.corners[(i + 1)%len(rect.corners)], color=color)

def update(x, y):
    mouse = coords_to_pos(x, y)

    draw.clear()

    rect0 = Rect(-100, -100, 200, 100, 30)
    rect1 = Rect(mouse.x, mouse.y, 250, 90, -15)

    if Rect.intersect(rect0, rect1):
        color = colors.red
    else:
        color = colors.green

    draw_rect(rect0, color)
    draw_rect(rect1, colors.blue)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    update(x, y)

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    update(x, y)


run()
