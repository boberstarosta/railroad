
from ..network.basetrackobject import BaseTrackObject
import railroad.network.scanners
from .wheel import Wheel
from .consist import Consist


class TrainCar(BaseTrackObject):

    coupling_length = 50

    def __init__(self, trains, model, parent_segment, t, rotated=False, parent_consist=None):
        super().__init__(trains.network, parent_segment, t, rotated)
        self.trains = trains
        self.model = model
        self._position = None
        self.sprite = model.create_sprite(trains.network.app.batch)
        self.wheels = []
        self.coupled_traincars = [None, None]
        self._direction = None
        self.velocity = -4500  # 162 km/h
        if parent_consist is None:
            self.parent_consist = Consist(trains)
        else:
            self.parent_consist = parent_consist
        self.parent_consist.traincars.append(self)
        trains.traincars.append(self)
        parent_segment.traincars.append(self)
        self._update_position()

    def delete(self):
        self.sprite.delete()
        self.parent_consist.traincars.remove(self)
        if len(self.parent_consist.traincars) == 0:
            self.parent_consist.delete()
        self.trains.traincars.remove(self)
        self.parent_segment.traincars.remove(self)
        super().delete()

    def on_parent_segment_changed(self, old_parent_segment, parent_segment):
        old_parent_segment.traincars.remove(self)
        parent_segment.traincars.append(self)

    def update_velocity(self, dt):
        if self.velocity == 0:
            return

        backwards = self.velocity < 0
        delta_pos = abs(self.velocity * dt)
        scan = railroad.network.scanners.Scanner(self.parent_segment, self.t, backwards, delta_pos)

        if backwards != scan.final_backwards:
            self.velocity *= -1
            self.rotated = not self.rotated

        self.parent_segment = scan.final_segment
        self._t = scan.final_t
        self._update_position()

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
            self.trains, model, scan.final_segment, scan.final_t, parent_consist=self.parent_consist)

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
        while len(self.wheels) > 0:
            self.wheels[-1].delete()

        scans = [
            railroad.network.scanners.DistanceScanner(self, backwards=not self.rotated),
            railroad.network.scanners.DistanceScanner(self, backwards=self.rotated),
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
