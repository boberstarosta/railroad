
import pyglet
from .basemode import BaseMode


class StraightenTrackMode(BaseMode):

    name = "Straighten track"

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_edge = self.app.network.get_nearest_edge(mouse, self.search_radius)
            if nearest_edge is not None:
                neighbors = []
                for n in nearest_edge.nodes:
                    neighbors.extend(n.other_edges(nearest_edge))
                has_straight_neighbors = True in [e.straight for e in neighbors]
                if (not nearest_edge.straight and not has_straight_neighbors) or (nearest_edge.straight and not has_straight_neighbors):
                    nearest_edge.straight = not nearest_edge.straight

