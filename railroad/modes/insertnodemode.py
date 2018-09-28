
import pyglet
from .basemode import BaseMode
from .. import geometry
from ..network.node import Node
from ..network.edge import Edge


class InsertNodeMode(BaseMode):
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_track_segment = self.app.network.get_nearest_track_segment(mouse, max_distance=self.search_radius)
            if nearest_track_segment is not None:
                old_edge = nearest_track_segment.parent_edge
                track_nodes = nearest_track_segment.nodes
                nodes = old_edge.nodes
                position = geometry.nearest_point_on_segment(mouse, track_nodes[0].position, track_nodes[1].position)
                too_close = True in [(n.position - position).length < self.min_track_length for n in nodes]
                if not too_close:
                    old_edge.delete()
                    new_node = Node(self.app.network, position)
                    Edge(self.app.network,  nodes[0], new_node, old_edge.straight)
                    Edge(self.app.network, new_node, nodes[1], old_edge.straight)

