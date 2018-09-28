
import pyglet
from .basemode import BaseMode


class SwitchJunctionMode(BaseMode):

    name = "Switch junction"

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_node = self.app.network.get_nearest_node(mouse, max_distance=self.search_radius)
            if nearest_node is not None:
                if len(nearest_node.edges) == 3:
                    nearest_node.switch()

