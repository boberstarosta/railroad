
from ..network.basetrackobject import BaseTrackObject
import railroad.network.scanners
from .wheel import Wheel


class TrainCar(BaseTrackObject):

    coupling_length = 50

    def __init__(self, trains, model, parent_segment, t, rotated=False):
        super().__init__(trains.network, parent_segment, t, rotated)
        self.trains = trains
        self.model = model
        self._position = None
        self.sprite = model.create_sprite(trains.network.app.batch)
        self.wheels = []
        self.coupled_traincars = [None, None]
        self._direction = None
        trains.traincars.append(self)
        parent_segment.traincars.append(self)
        self._update_position()

    def delete(self):
        super().delete()
        self.sprite.delete()
        self.trains.traincars.remove(self)
        self.parent_segment.traincars.remove(self)

    def update(self, dt):
        pass

    def couple_new_traincar(self, model, coupled_index):
        if self.coupled_traincars[coupled_index] is not None:
            print("TrainCar.couple_new_traincar: Coupling {} already taken.".format(coupled_index))
            return

        scan = railroad.network.scanners.Scanner(
            self.parent_segment, self.t, coupled_index == 0 and not self.rotated,
            self.model.length/2 + self.coupling_length + model.length/2
        )

        if scan.final_segment is None:
            print("TrainCar.couple_new_traincar: Ran out of track.")

        new_traincar = TrainCar(
            self.trains, model, scan.final_segment, scan.final_t)

        self.coupled_traincars[coupled_index] = new_traincar

        new_coupled_index = 1 if scan.final_backwards else 0
        new_traincar.coupled_traincars[new_coupled_index] = self

        print("\n".join([
            "TrainCar.couple_new_traincar complete. Status:",
            "self rotated: {}".format(self.rotated),
            "coupled index: {}".format(coupled_index),
            "new rotated: {}".format(new_traincar.rotated),
            "new_coupled_index: {}".format(new_coupled_index),
        ]))

    def _update_position(self):
        for wheel in self.wheels:
            wheel.delete()

        scans = [
            railroad.network.scanners.DistanceScanner(self, backwards=True),
            railroad.network.scanners.DistanceScanner(self, backwards=False),
        ]

        for scan in scans:
            self.wheels.append(Wheel(
                self,
                scan.final_segment,
                scan.final_t,
                False
            ))

        self._position = (self.wheels[0].position + self.wheels[1].position) / 2
        self.sprite.position = self._position
        self._direction = (self.wheels[1].position - self.wheels[0].position).normalized
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
