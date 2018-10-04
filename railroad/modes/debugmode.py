
import pyglet
from .basemode import BaseMode
from .. import graphics
from .. import geometry


class DebugMode(BaseMode):
    name = "Debug"

    def __init__(self, app):
        super().__init__(app)
        self.label = pyglet.text.Label(
            "", font_name="mono", font_size=10, color=(255, 255, 255, 255),
            x=self.app.window.width/2 - 200, y=self.app.window.height-20,
            width=400, multiline=True, group=graphics.group.gui_front,
            batch=self.app.gui.batch
        )
        self.mouse = self.app.camera.to_world(0, 0)
        self.nearest_segment = None
        self.nearest_t = None

    def on_delete(self):
        self.label.delete()

    def update(self, x, y):
        self.mouse = self.app.camera.to_world(x, y)
        self.nearest_segment = self.app.network.get_nearest_track_segment(self.mouse, self.search_radius)
        if self.nearest_segment is not None:
            self.nearest_t = geometry.nearest_t_on_line(
                self.mouse, self.nearest_segment.nodes[0].position, self.nearest_segment.nodes[1].position)
        else:
            self.nearest_t = None

        self.label.text = "\n".join([
            "len(traincars): {}".format(len(self.app.trains.traincars)),
            "segment: {}".format(self.nearest_segment),
            "t: {}".format(self.nearest_t),
        ])

    def on_mouse_motion(self, x, y, dx, dy):
        self.update(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.update(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            pass
