
import pyglet
from .basemode import BaseMode
from ..network.edge import Edge


class RemoveNodeMode(BaseMode):
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_node = self.app.network.get_nearest_node(mouse, max_distance=self.search_radius)
            if nearest_node is not None:
                if len(nearest_node.edges) == 2:
                    other_nodes = nearest_node.nodes
                    has_all_straight = False not in [e.straight for e in nearest_node.edges]
                    for edge in nearest_node.edges:
                        edge.delete()
                    new_edge = Edge(self.app.network, other_nodes[0], other_nodes[1], straight=has_all_straight)
                    nearest_node.delete()

