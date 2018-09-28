
import pyglet
from .basemode import BaseMode


class RotateTrackObjectMode(BaseMode):
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_signal = self.app.network.get_nearest_track_object(mouse, max_distance=self.search_radius)
            if nearest_signal is not None:
                nearest_signal.rotated = not nearest_signal.rotated

