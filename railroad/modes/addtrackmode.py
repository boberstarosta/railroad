
import pyglet
from .basemode import BaseMode
from ..network.node import Node
from ..network.edge import Edge


class AddTrackMode(BaseMode):
    
    def __init__(self, app):
        super().__init__(app)
        self.start_node = None
        self.end_node = None
        self.new_edge = None
        self.new_edge_straight = False
        self.end_node_existing = None
    
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        mouse = self.app.camera.to_world(x, y)
        
        if buttons & pyglet.window.mouse.LEFT and self.start_node is not None:
            if self.end_node is None:
                if self.end_node_existing is None:
                    nearest_node = self.app.network.get_nearest_node(
                        mouse,
                        excluded = [self.start_node] + self.start_node.connected_nodes,
                        max_distance = self.search_radius)
                    
                    if nearest_node is not None and nearest_node.has_free_connections:
                        nearest_connectable_node = nearest_node
                    else:
                        nearest_connectable_node = None
                    
                    if nearest_connectable_node is None:
                        self.end_node = Node(self.app.network, mouse)
                        self.new_edge = Edge(self.app.network, self.start_node, self.end_node, self.new_edge_straight)
                    else:
                        self.end_node_existing = nearest_connectable_node
                        self.new_edge = Edge(self.app.network, self.start_node, self.end_node_existing)
                else: #  Existing end node is not None
                    if (mouse - self.end_node_existing.position).length > self.search_radius:
                        self.end_node_existing = None
                        self.end_node = Node(self.app.network, mouse)
                        self.new_edge.delete()
                        self.new_edge = Edge(self.app.network, self.start_node, self.end_node, self.new_edge_straight)
            else: #  End node is not None
                nearest_node = self.app.network.get_nearest_node(
                    mouse,
                    excluded = [self.start_node, self.end_node] + self.start_node.connected_nodes,
                    max_distance = self.search_radius)
                
                if nearest_node is not None and nearest_node.has_free_connections:
                    nearest_connectable_node = nearest_node
                else:
                    nearest_connectable_node = None
                
                if nearest_connectable_node is None:
                    self.end_node.position = mouse
                else:
                    self.end_node.delete()
                    self.end_node = None
                    self.end_node_existing = nearest_connectable_node
                    self.new_edge.delete()
                    self.new_edge = Edge(self.app.network, self.start_node, self.end_node_existing)
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        mouse = self.app.camera.to_world(x, y)
        nearest_node = self.app.network.get_nearest_node(mouse, max_distance=self.search_radius)
        
        if buttons & pyglet.window.mouse.LEFT:
            if nearest_node is None:
                self.start_node = Node(self.app.network, mouse)
                self.new_edge_straight = True
            elif nearest_node.has_free_connections:
                self.start_node = nearest_node
                if True in [e.straight for e in nearest_node.edges]:
                    self.new_edge_straight = False
                else:
                    self.new_edge_straight = True
    
    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            if self.new_edge is not None and self.new_edge.length < self.min_track_length:
                self.new_edge.delete()
            if self.start_node is not None and len(self.start_node.edges) == 0:
                self.start_node.delete()
            if self.end_node is not None and len(self.end_node.edges) == 0:
                self.end_node.delete()
            self.start_node = None
            self.end_node = None
            self.end_node_existing = None
            self.new_edge = None

