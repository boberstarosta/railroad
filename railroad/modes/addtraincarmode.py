
from .. import geometry
from ..trains.models import *
from ..trains.traincar import TrainCar
from ..trains.wheel import Wheel
from ..trains.coupling import Coupling
from ..network.scanners import TrackObjectScanner
from .basemode import BaseMode


class AddTrainCarMode(BaseMode):
    name = "Add train car"

    def __init__(self, app):
        super().__init__(app)
        self.traincar_model = TrainCarBulk

    def add_traincar(self, segment, t):

        wheel_scans = [
            TrackObjectScanner(segment, t, True, Wheel),
            TrackObjectScanner(segment, t, False, Wheel),
        ]
        traincar_scans = [
            TrackObjectScanner(segment, t, True, TrainCar),
            TrackObjectScanner(segment, t, False, TrainCar),
        ]

        for i, (traincar_scan, wheel_scan) in enumerate(zip(traincar_scans, wheel_scans)):
            if traincar_scan.final_object is not None:
                traincar = traincar_scan.final_object
                wheel = wheel_scan.final_object
                min_length = self.traincar_model.length/2 + Coupling.length + traincar.model.length/2
                if traincar_scan.length_travelled < min_length:
                    other_tcs = traincar_scans[(i + 1)%2]
                    if other_tcs.final_object is not None:
                        other_min_length =\
                            self.traincar_model.length/2 + Coupling.length + other_tcs.final_object.model.length/2
                        if other_tcs.length_travelled < other_min_length:
                            print("Both too close")
                            return
                    print("One too close")
                    couple_index = 0 if wheel is traincar.wheels[0] else 1
                    traincar.couple_new_traincar(self.traincar_model, couple_index)
                    return

        TrainCar(self.app.trains, self.traincar_model, segment, t)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_segment = self.app.network.get_nearest_track_segment(mouse, max_distance=self.search_radius)
            if nearest_segment is not None:
                t = geometry.nearest_t_on_line(mouse, nearest_segment.nodes[0].position,
                                               nearest_segment.nodes[1].position)
                if 0 <= t <= 1:
                    self.add_traincar(nearest_segment, t)
