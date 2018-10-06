
from pyglet.gl import *
from railroad.vec import Vec


window = pyglet.window.Window(width=1200, height=800)


class colors:
    red = (1.0, 0.0, 0.0, 1.0)
    green = (0.0, 1.0, 0.0, 1.0)
    blue = (0.0, 0.0, 1.0, 1.0)
    yellow = (1.0, 1.0, 0.0, 1.0)
    orange = (1.0, 0.5, 0.0, 1.0)
    magenta = (1.0, 0.0, 1.0, 1.0)
    cyan = (0.0, 1.0, 1.0, 1.0)
    grey = (0.5, 0.5, 0.5, 1.0)


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
            glVertex2f(*(start + vector.normalized * length))
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
        cls.points.append((pos, color))

    @classmethod
    def vec(cls, start, vector, l=30, color=colors.grey):
        cls.vectors.append((start, vector, l, color))

    @classmethod
    def line(cls, start, end, color=colors.grey):
        cls.lines.append((start, end, color))


def setup_projection():
    glViewport(0, 0, window.width, window.height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-window.width / 2, window.width / 2, -window.height / 2, window.height / 2)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

@window.event
def on_draw():
    window.clear()
    setup_projection()
    draw.draw()

def coords_to_pos(x, y):
    return Vec(x-window.width//2, y-window.height//2)

def run():
    pyglet.app.run()
