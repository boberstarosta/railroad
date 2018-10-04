
from .basetrackobject import BaseTrackObject


class StaticTrackObject(BaseTrackObject):

    def __init__(self, network, parent_segment, t, rotated):
        super().__init__(network, parent_segment, t, rotated)
        self.network.static_track_objects.append(self)
        self.parent_segment.static_track_objects.append(self)

    def delete(self):
        super().delete()
        self.network.static_track_objects.remove(self)
        self.parent_segment.static_track_objects.remove(self)

    @property
    def position(self):
        vector = self.parent_segment.nodes[1].position - self.parent_segment.nodes[0].position
        return self.parent_segment.nodes[0].position + vector * self._t
