
import pyglet
from .. import graphics
from .. import geometry


class Panel:

    color_fill=  (127, 127, 127, 95)
    color_frame = (192, 192, 192, 255)

    width = 300

    def __init__(self, gui):
        self.gui = gui
        vertices = self._generate_vertices(gui.app.window.width, gui.app.window.width)
        self.vertex_list_fill = self.gui.batch.add(
            4, pyglet.gl.GL_QUADS, graphics.group.gui_back, ("v2i", vertices), ("c4B", self.color_fill*4))
        self.vertex_list_frame = self.gui.batch.add(
            4, pyglet.gl.GL_LINE_LOOP, graphics.group.gui_front, ("v2i", vertices), ("c4B", self.color_frame*4))
        self.rect = self.get_rect(vertices)
        gui.app.window.push_handlers(self.on_resize, self.on_mouse_press)

    def _generate_vertices(self, width, height):
        return (
            width - 1 - self.width, 0,
            width - 1 - self.width, height - 1,
            width - 1, height - 1,
            width, 0
        )

    def get_rect(self, vertices):
        return vertices[0], vertices[1], vertices[4] - vertices[0], vertices[5] - vertices[1]

    def on_resize(self, width, height):
        vertices = self._generate_vertices(width, height)
        self.vertex_list_fill.vertices = self.vertex_list_frame.vertices = vertices
        self.rect = self.get_rect(vertices)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT and geometry.point_in_rect((x, y), *self.rect):
            return pyglet.event.EVENT_HANDLED

    def update(self, dt):
        pass
