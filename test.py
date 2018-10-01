#!/usr/bin/env python3

from pyglet.gl import *
from railroad.geometry import *


window = pyglet.window.Window(width=1200, height=800)

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

def setup_projection():
    glViewport(0, 0, window.width, window.height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-window.width/2, window.width/2, -window.height/2, window.height/2)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def update(x, y):
    mouse = Vec(x-window.width//2, y-window.height//2)

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

@window.event
def on_draw():
    window.clear()
    setup_projection()
    draw.draw()
    

pyglet.app.run()
