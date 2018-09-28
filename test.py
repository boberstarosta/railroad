#!/usr/bin/env python3

import math
import pyglet
from pyglet.gl import *
from railroad.vec import Vec
from railroad.geometry import *


window = pyglet.window.Window(width=1200, height=800)

points = [
    Vec(-400, 200),
    Vec(-200, 250),
    Vec(200, 100),
    Vec(100, -330),
]
steps = 10
curve = None
segments = []

class colors:
    red    = (1.0, 0.0, 0.0, 1.0)
    green  = (0.0, 1.0, 0.0, 1.0)
    blue   = (0.0, 0.0, 1.0, 1.0)
    yellow = (1.0, 1.0, 0.0, 1.0)
    orange = (1.0, 0.5, 0.0, 1.0)
    magenta= (1.0, 0.0, 1.0, 1.0)
    cyan   = (0.0, 1.0, 1.0, 1.0)
    grey   = (0.5, 0.5, 0.5, 1.0)

class draw:
    points = []
    vectors = []
    lines = []
    
    @classmethod
    def clear(cls):
        cls.points = []
        cls.vectors = []
        cls.lines = []
    
    @classmethod
    def draw(cls):
        glPointSize(7)
        glBegin(GL_POINTS)
        for point, color in cls.points:
            glColor4f(*color)
            glVertex2f(*point)
        glEnd()
        
        glPointSize(5)
        for start, vector, length, color in cls.vectors:
            glColor4f(*color)
            glBegin(GL_LINES)
            glVertex2f(*start)
            glVertex2f(*(start + vector*length))
            glEnd()
            glBegin(GL_POINTS)
            glVertex2f(*start)
            glEnd()
        
        glBegin(GL_LINES)
        for start, end, color in cls.lines:
            glColor4f(*color)
            glVertex2f(*start)
            glVertex2f(*end)
        glEnd()
    
    @classmethod
    def pt(cls, pos, color=colors.grey):
        cls.points.append( (pos, color) )
    @classmethod
    def vec(cls, start, vector, l=30, color=colors.grey):
        cls.vectors.append( (start, vector, l, color) )
    @classmethod
    def line(cls, start, end, color=colors.grey):
        cls.lines.append( (start, end, color) )

def draw_curve():
    glPointSize(9)
    glColor4f(*colors.red)
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(*p)    
    glEnd()
    
    glColor4f(*colors.grey)
    glBegin(GL_LINE_STRIP)
    for p in curve:
        glVertex2f(*p)
    glEnd()
    
    glColor4f(*colors.grey)
    for seg in segments:
        glBegin(GL_LINE_LOOP)
        for p in seg:
            glVertex2f(*p)
        glEnd()

def setup_projection():
    glViewport(0, 0, window.width, window.height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-window.width/2, window.width/2, -window.height/2, window.height/2)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def create_segment(curve, index):
    width = 40
    
    p0 = None if index < 1 else curve[index - 1]
    p1 = curve[index]
    p2 = curve[index + 1]
    p3 = None if index >= len(curve) - 2 else curve[index + 2]
    
    dir12 = (p2 - p1).normalized
    dir12perp = Vec(-dir12.y, dir12.x)
    
    l_start = p1 + dir12perp * width/2
    r_start = p1 - dir12perp * width/2
    
    if p0 is None:
        l1 = l_start
        r1 = r_start
    else:
        p0p2dir = (p2 - p0).normalized
        side1dir = Vec(-p0p2dir.y, p0p2dir.x)
        l1 = intersect_point(l_start, dir12, p1, side1dir)
        r1 = intersect_point(r_start, dir12, p1, side1dir)
    
    if p3 is None:
        l2 = p2 + dir12perp * width/2
        r2 = p2 - dir12perp * width/2
    else:
        p1p3dir = (p3 - p1).normalized
        side2dir = Vec(-p1p3dir.y, p1p3dir.x)
        l2 = intersect_point(l_start, dir12, p2, side2dir)
        r2 = intersect_point(r_start, dir12, p2, side2dir)
        draw.line(l2, r2, color=colors.green)
        
    return [r1, r2, l2, l1]

def update_curve():
    global curve, segments
    draw.clear()
    curve = [bezier3(*points, i/steps) for i in range(steps+1)]
    
    segments = []
    
    for i in range(len(curve) - 1):
        segments.append( create_segment(curve, i) )

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    mouse = Vec(x-window.width//2, y-window.height//2)
    nearest_index = -1
    shortest_dist = float("inf")
    for i, p in enumerate(points):
        dist = (p - mouse).length
        if dist < shortest_dist and dist < 40:
            shortest_dist = dist
            nearest_index = i
    if nearest_index >= 0:
        points[nearest_index] = mouse
        update_curve()

@window.event
def on_draw():
    window.clear()
    setup_projection()
    draw_curve()
    draw.draw()
    

update_curve()
pyglet.app.run()

