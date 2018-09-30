
from .baseedge import BaseEdge
from .tracknode import TrackNode
from .tracksegment import TrackSegment
from .. import geometry
from ..trackrenderer import TrackRenderer


class Edge(BaseEdge):
    
    def __init__(self, network, node1, node2, straight=False):
        self._straight = straight
        super().__init__(node1, node2)
        
        self.network = network        
        self.track_nodes = []
        self.track_segments = []
        self.renderer = TrackRenderer(self)
        self.update_track()
        self.renderer.update_track()
        self.network.edges.append(self)

        # Update track for all connected edges
        for node in self.nodes:
            # First update the actual track
            for other_edge in node.other_edges(self):
                other_edge.update_track()
            # Only then update renderer to include changes in common nodes
            for other_edge in node.other_edges(self):
                other_edge.renderer.update_track()

    def delete(self):
        super().delete()
        self.network.edges.remove(self)
        self._delete_track()
        self.renderer.delete()

    def _delete_track(self):
        for track_node in self.track_nodes:
            track_node.delete()
        self.track_nodes = []
        
        for track_segment in self.track_segments:
            track_segment.delete()
        self.track_segments = []
        self.renderer.clear()
    
    def _create_track(self, points):
        self.track_nodes = [TrackNode(self.network, None, p) for p in points]
        tns = [self.nodes[0].track_node] + self.track_nodes + [self.nodes[1].track_node]
        self.track_segments = [TrackSegment(self.network, self, tns[i], tns[i+1]) for i in range(len(tns) - 1)]

    def _directions(self):
        this_dirs = []
        result = []
        for i in range(2):
            this_dirs.append((self.nodes[(i+1)%2].position - self.nodes[i].position).normalized)
            other_edge = self.nodes[i].other_edge(self)
            if other_edge is None:
                result.append(this_dirs[i])
            elif other_edge.straight:
                other_node = other_edge.other_node(self.nodes[i])
                result.append((self.nodes[i].position - other_node.position).normalized)
            else:
                other_node = other_edge.other_node(self.nodes[i])
                other_dir = (other_node.position - self.nodes[i].position).normalized
                result.append((this_dirs[i] - other_dir).normalized)
        
        return result
    
    def update_track(self):
        self._delete_track()
        
        connected_edges = [n.other_edge(self) for n in self.nodes if n.other_edge is not None]
        
        if self.straight or len(connected_edges) == 0:
            points = []
        else:
            directions = self._directions()
            points = geometry.generate_curve(
                self.nodes[0].position, directions[0],
                self.nodes[1].position, directions[1],
                precision=5)
        
        self._create_track(points)
    
    @property
    def straight(self):
        return self._straight

    @straight.setter
    def straight(self, value):
        if value != self._straight:
            self._straight = value
            self.update_track()
            for node in self.nodes:
                for other_edge in node.other_edges(self):
                    other_edge.update_track()
            self.renderer.update_track()
            for node in self.nodes:
                for other_edge in node.other_edges(self):
                    other_edge.renderer.update_track()
