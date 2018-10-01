
from ..geometry import dist_to_segment
from .signal import Signal


class Network:
    def __init__(self, app):
        self.app = app
        self.nodes = []
        self.edges = []
        self.track_nodes = []
        self.track_segments = []
        self.track_objects = []
        self.scenery_objects = []
        self._show_nodes = True
    
    def update(self, dt):
        if self.show_nodes:
            for node in self.nodes:
                node.sprite.rotation -= dt * 90.0
        for to in self.track_objects:
            to.update(dt)
    
    def get_nearest_node(self, position, excluded=None, max_distance=40):
        if excluded is None:
            excluded = []
        max_distance_sq = max_distance**2
        nearest_node = None
        shortest_distance_sq = float("inf")
        for node in [n for n in self.nodes if n not in excluded]:
            distance_sq = (node.position - position).length_sq
            if distance_sq < shortest_distance_sq and distance_sq <= max_distance_sq:
                nearest_node = node
                shortest_distance_sq = distance_sq
        return nearest_node
    
    def get_nearest_edge(self, position, max_distance=40):
        nearest_segment = self.get_nearest_track_segment(position, max_distance)        
        return None if nearest_segment is None else nearest_segment.parent_edge
    
    def get_nearest_track_segment(self, position, max_distance=40):
        nearest_segment = None
        shortest_distance = float("inf")
        for track_segment in self.track_segments:
            distance = dist_to_segment(position, track_segment.nodes[0].position, track_segment.nodes[1].position)
            if distance < shortest_distance and distance <= max_distance:
                nearest_segment = track_segment
                shortest_distance = distance
        return nearest_segment
    
    def get_nearest_track_object(self, position, to_type=None, max_distance=40):
        nearest_to = None
        shortest_distance = float("inf")
        valid_tos = self.track_objects if to_type is None else [to for to in self.track_objects if isinstance(to, to_type)]
        for to in valid_tos:
            distance = (position - to.position).length
            if distance < shortest_distance and distance <= max_distance:
                nearest_to = to
                shortest_distance = distance
        return nearest_to

    def get_nearest_scenery_object(self, position, excluded=None, max_distance=40):
        if excluded is None:
            excluded = []
        max_distance_sq = max_distance**2
        nearest_so = None
        shortest_distance_sq = float("inf")
        for so in [o for o in self.scenery_objects if o not in excluded]:
            distance_sq = (so.position - position).length_sq
            if distance_sq < shortest_distance_sq and distance_sq <= max_distance_sq:
                nearest_so = so
                shortest_distance_sq = distance_sq
        return nearest_so

    @property
    def signals(self):
        return [to for to in self.track_objects if isinstance(to, Signal)]
    
    @property
    def show_nodes(self):
        return self._show_nodes
    
    @show_nodes.setter
    def show_nodes(self, value):
        if value != self._show_nodes:
            self._show_nodes = value
            for node in self.nodes:
                node.sprite.visible = self._show_nodes

