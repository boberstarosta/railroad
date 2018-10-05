
from ..network.basetrackobject import BaseTrackObject
from .consist import Consist
import railroad.network.scanners
from .coupling import Coupling


class TrainCar(BaseTrackObject):

    def __init__(self, trains, model, parent_segment, t, rotated=False, coupling0=None, coupling1=None):
        super().__init__(trains.network, parent_segment, t, rotated)
        self.trains = trains
        self.model = model
        self._position = None
        self.parent_consist = Consist(trains)
        self.sprite = model.create_sprite(trains.network.app.batch)
        self._wheel_positions = [None, None]
        self._direction = None
        if coupling0 is None:
            coupling0 = Coupling(trains, self)
        if coupling1 is None:
            coupling1 = Coupling(trains, self)
        self.couplings = [coupling0, coupling1]
        trains.traincars.append(self)
        parent_segment.traincars.append(self)
        self.parent_consist.traincars.append(self)
        self._update_position()

    def delete(self):
        super().delete()
        self.sprite.delete()
        self.trains.traincars.remove(self)
        self.parent_segment.traincars.remove(self)
        self.parent_consist.traincars.remove(self)
        for coupling in self.couplings:
            if coupling is not None:
                coupling.traincars.remove(self)
                if len(coupling.traincars) == 0:
                    coupling.delete()

    def update(self, dt):
        pass

    def _get_wheel_points(self):
        track_back = railroad.network.scanners.DistanceScanner(self, backwards=True)
        track_front = railroad.network.scanners.DistanceScanner(self, backwards=False)
        return (track_back.final_segment.position_from_t(track_back.final_t),
                track_front.final_segment.position_from_t(track_front.final_t))

    def _update_position(self):
        self._wheel_positions = self._get_wheel_points()
        self._position = (self._wheel_positions[0] + self._wheel_positions[1]) / 2
        self.sprite.position = self._position
        self._direction = (self._wheel_positions[1] - self._wheel_positions[0]).normalized
        self.sprite.rotation = -self._direction.angle

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        if value != self._t:
            self._t = value
            self._update_position()

    @property
    def position(self):
        return self._position

    @property
    def direction(self):
        return self._direction
