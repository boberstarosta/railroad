
import pyglet
from .basemode import BaseMode


class RemoveTrackObjectMode(BaseMode):

    name = "Remove track object"

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_to = self.app.network.get_nearest_track_object(mouse, max_distance=self.search_radius)
            if nearest_to is not None:
                nearest_to.delete()
