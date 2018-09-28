
import pyglet
from .basemode import BaseMode
from .. import geometry


class MoveTrackMode(BaseMode):
    
    def __init__(self, app):
        super().__init__(app)
        self.active_node = None
    
    def calculate_position(self, mouse, node):
        node_is_final_straight = len(node.edges) == 1 and node.edges[0].straight
        node_is_mid_straight = 2 <= len(node.edges) <= 3 and node.straight.straight and node.point.straight
        node_is_half_straight = 2 <= len(node.edges) <= 3 \
            and ((not node.straight.straight and node.point.straight) or (node.straight.straight and not node.point.straight))
        if node_is_final_straight:
            edge = node.edges[0]
            next_node = edge.other_node(node)
            if len(next_node.other_edges(edge)) > 0:
                next_edge = next_node.other_edge(edge)
                if next_edge.straight:
                    t = geometry.nearest_t_on_line(mouse, next_node.position, node.position)
                    length = (next_node.position - node.position).length
                    if t * length >= self.min_track_length:
                        return geometry.nearest_point_on_line(mouse, next_node.position, node.position)
                    else:
                        return node.position
                else:
                    return mouse
            else:
                return mouse
        elif node_is_mid_straight:
            prev_node = node.point.other_node(node)
            next_node = node.straight.other_node(node)
            length = (next_node.position - prev_node.position).length
            t = geometry.nearest_t_on_line(mouse, prev_node.position, next_node.position)
            if self.min_track_length <= t * length <= length - self.min_track_length:
                return geometry.nearest_point_on_segment(mouse, prev_node.position, next_node.position)
            else:  # Too close to other nodes
                return node.position
        elif node_is_half_straight:
            straight_edge = [e for e in node.edges if e.straight][0]
            straight_node = straight_edge.other_node(node)
            next_edge = straight_node.other_edge(straight_edge)
            if next_edge is not None and next_edge.straight:
                t = geometry.nearest_t_on_line(mouse, straight_node.position, node.position)
                length = (straight_node.position - node.position).length
                if t * length >= self.min_track_length:
                    return geometry.nearest_point_on_line(mouse, straight_node.position, node.position)
                else:
                    return node.position
            else:
                return mouse
        else:
            return mouse
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        mouse = self.app.camera.to_world(x, y)
        
        if buttons & pyglet.window.mouse.LEFT:
            if self.active_node is not None:
                self.active_node.position = self.calculate_position(mouse, self.active_node)
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            self.active_node = self.app.network.get_nearest_node(mouse, max_distance=self.search_radius)
    
    def on_mouse_release(self, x, y, buttons, modifiers):
        self.active_node = None

