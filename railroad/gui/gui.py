import pyglet
from pyglet.gl import *
from .. import geometry


class Gui:
    def __init__(self, app):
        self.app = app
        self.app.window.push_handlers(self)
        self.batch = pyglet.graphics.Batch()
        self.rect = (0, 0, app.window.width, 100)
        vertices = [self.rect[i] for i in [0, 1, 0, 3, 2, 3, 2, 0]]
        self.batch.add(4, GL_QUADS, None, ("v2i", vertices))

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            if geometry.point_in_rect((x, y), *self.rect):
                print("click!")

    def draw(self):
        self.batch.draw()
