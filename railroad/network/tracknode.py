
from .basenode import BaseNode


class TrackNode(BaseNode):
    
    def __init__(self, network, parent_node, position):
        super().__init__(position)
        self.network = network
        self.parent_node = parent_node
        self.network.track_nodes.append(self)
    
    def delete(self):
        super().delete()
        self.network.track_nodes.remove(self)
    
    def _segment_from_edge(self, edge):        
        if edge is None:
            return None
        for segment in edge.track_segments:
            if segment in self.edges:
                return segment
        raise ValueError("TrackNode._segment_from_edge:  segment not found")
    
    def other_segment(self, segment):
        if segment not in self.edges:
            raise ValueError("TrackNode.other_segment: Not my segment")
        if self.parent_node is None:
            if len(self.edges) < 2:
                return None
            else:
                return [e for e in self.edges if e is not segment][0]
        point = self.point
        if segment is point:
            return self.current_edge_set
        else:
            return point

    @property
    def is_switched(self):
        return self.parent_node._is_switched
    
    @property
    def current_edge_set(self):
        return self._segment_from_edge(self.parent_node.current_edge_set)

    @property
    def point(self):
        return self._segment_from_edge(self.parent_node.point)
    
    @property
    def straight(self):
        return self._segment_from_edge(self.parent_node.straight)
    
    @property
    def turn(self):
        return self._segment_from_edge(self.parent_node.turn)

