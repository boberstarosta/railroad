
from ..network.basetrackobject import BaseTrackObject


class Wheel(BaseTrackObject):

    def __init__(self, parent_traincar, parent_segment, t, rotated):
        super().__init__(parent_segment.network, parent_segment, t, rotated)
        self.parent_traincar = parent_traincar
        self.position = parent_segment.position_from_t(t)

    def delete(self):
        super().delete()
        self.parent_traincar.wheels.remove(self)
