
from ..network.basetrackobject import BaseTrackObject
from .consist import Consist
from .distancetrackfollower import DistanceTrackFollower


class TrainCar(BaseTrackObject):

    def __init__(self, trains, model, parent_segment, t, rotated=False, parent_consist=None):
        super().__init__(trains.network, parent_segment, t, rotated)
        self.trains = trains
        self.model = model
        self._position = None
        if parent_consist is None:
            parent_consist = Consist(trains)
        self.parent_consist = parent_consist
        self.sprite = model.create_sprite(trains.network.app.batch)
        trains.traincars.append(self)
        parent_segment.traincars.append(self)
        self._update_position()

    def delete(self):
        super().delete()
        self.sprite.delete()
        self.trains.traincars.remove(self)
        self.parent_segment.traincars.remove(self)
        self.parent_consist.traincars.remove(self)

    def update(self, dt):
        pass

    def _get_wheel_points(self):
        track_back = DistanceTrackFollower(self, backwards=True)
        track_front = DistanceTrackFollower(self, backwards=False)
        return track_back.found_segment.position_from_t(track_back.found_t),\
               track_front.found_segment.position_from_t(track_front.found_t)

    def _update_position(self):
        wheel0, wheel1 = self._get_wheel_points()
        self._position = (wheel0 + wheel1) / 2
        self.sprite.position = self._position
        self.sprite.rotation = -(wheel1 - wheel0).angle

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
