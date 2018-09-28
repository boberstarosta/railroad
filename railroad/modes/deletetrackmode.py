
import pyglet
from .basemode import BaseMode


class DeleteTrackMode(BaseMode):
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_edge = self.app.network.get_nearest_edge(mouse, max_distance=self.search_radius)
            if nearest_edge is not None:
                nodes = nearest_edge.nodes
                nearest_edge.delete()
                for node in nodes:
                    if len(node.edges) == 0:
                        node.delete()

