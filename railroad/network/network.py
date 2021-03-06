
from ..geometry import dist_to_segment_sq


class Network:
    def __init__(self, app):
        self.app = app
        self.nodes = []
        self.edges = []
        self.track_nodes = []
        self.track_segments = []
        self.static_track_objects = []
        self.scenery_objects = []
        self._show_nodes = True
    
    def update(self, dt):
        if self.show_nodes:
            for node in self.nodes:
                node.sprite.rotation -= dt * 90.0
        for to in self.static_track_objects:
            to.update(dt)

    def clear(self):
        # Clear the network - edges, nodes, track objects
        while len(self.edges) > 0:
            self.edges[-1].delete()
        while len(self.nodes) > 0:
            self.nodes[-1].delete()
        while len(self.scenery_objects) > 0:
            self.scenery_objects[-1].delete()

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
        max_distance_sq = max_distance**2
        nearest_segment = None
        shortest_distance_sq = float("inf")
        for track_segment in self.track_segments:
            distance_sq = dist_to_segment_sq(position, track_segment.nodes[0].position, track_segment.nodes[1].position)
            if distance_sq < shortest_distance_sq and distance_sq <= max_distance_sq:
                nearest_segment = track_segment
                shortest_distance_sq = distance_sq
        return nearest_segment
    
    def get_nearest_track_object(self, position, max_distance=40):
        nearest_to = None
        shortest_distance = float("inf")
        for to in self.static_track_objects:
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
    def show_nodes(self):
        return self._show_nodes
    
    @show_nodes.setter
    def show_nodes(self, value):
        if value != self._show_nodes:
            self._show_nodes = value
            for node in self.nodes:
                node.sprite.visible = self._show_nodes
