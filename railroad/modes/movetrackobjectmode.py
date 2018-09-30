
import pyglet
from .. import geometry
from .basemode import BaseMode


class MoveTrackObjectMode(BaseMode):

    name = "Move track object"

    def __init__(self, app):
        super().__init__(app)
        self.active_to = None

    def apply_position(self, mouse, to):
        nearest_segment = self.app.network.get_nearest_track_segment(mouse, max_distance=self.search_radius)
        if nearest_segment is not None:
            nearest_t = geometry.nearest_t_on_line(
                mouse,
                nearest_segment.nodes[0].position,
                nearest_segment.nodes[1].position,
            )
            if 0 <= nearest_t < 1:
                to_class = type(self.active_to)
                rotated = self.active_to.rotated
                self.active_to.delete()
                self.active_to = to_class(self.app.network, nearest_segment, nearest_t)
                self.active_to.rotated = rotated

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        mouse = self.app.camera.to_world(x, y)

        if buttons & pyglet.window.mouse.LEFT:
            if self.active_to is not None:
                self.apply_position(mouse, self.active_to)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            self.active_to = self.app.network.get_nearest_track_object(mouse, max_distance=self.search_radius)

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.active_to = None
