
import pyglet

from .baseedge import BaseEdge
from .. import graphics
from ..geometry import intersect_point
from ..vec import Vec


class TrackSegment(BaseEdge):
    
    def __init__(self, network, parent_edge, node1, node2):
        super().__init__(node1, node2)
        self.network = network
        self.parent_edge = parent_edge
        self.track_objects = []
        self.network.track_segments.append(self)
    
    def delete(self):
        super().delete()
        self.network.track_segments.remove(self)
        while len(self.track_objects) > 0:
            self.track_objects[-1].delete()
    
    @staticmethod
    def _is_valid_signal(to, to_classes, rotated, min_t, max_t, exclude):
        return (
            type(to) in to_classes
            and to.rotated == rotated
            and (min_t is None or to.t >= min_t)
            and (max_t is None or to.t <= max_t)
            and to not in exclude
        )
    
    def nearest_track_object(self, node, *to_classes, min_t=None, max_t=None, exclude=None):
        if exclude is None:
            exclude = []
        if node is self.nodes[0]:
            rotated = False
        elif node is self.nodes[1]:
            rotated = True
        else:
            raise ValueError("TrackSegment.nearest_signal:  Not my node.")
        valid_objects = [to for to in self.track_objects if self._is_valid_signal(to, to_classes, rotated, min_t, max_t, exclude)]
        if len(valid_objects) > 0:
            valid_objects.sort(key=lambda to: to.t, reverse=rotated)
            return valid_objects[0]
        else:
            return None
