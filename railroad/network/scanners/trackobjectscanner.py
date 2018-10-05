
from .basescanner import BaseScanner
import railroad.network.basetrackobject


class TrackObjectScanner(BaseScanner):
    """Follows track until first instance of one of to_classes is found"""

    def __init__(self, segment, t, backwards, *to_classes):
        for to_class in to_classes:
            if not issubclass(to_class, railroad.network.basetrackobject.BaseTrackObject):
                raise("TrackObjectScanner: class {} is not derived from BaseTrackObject.".format(to_class))

        self.to_classes = to_classes
        self.final_object = None
        self.length_travelled = 0
        self.run(segment, t, backwards)

    def check_segment(self, current_segment, node, min_t, max_t):
        self.final_object = current_segment.nearest_track_object(node, *self.to_classes, min_t=min_t, max_t=max_t)
        if self.final_object is not None:
            if node is current_segment.nodes[0]:
                delta_t = self.final_object.t - min_t
            else:
                delta_t = max_t - self.final_object.t
            self.length_travelled += delta_t * current_segment.length
            return True
        self.length_travelled += (max_t - min_t) * current_segment.length
