
from .. import geometry
from ..trains.models import *
from ..trains.traincar import TrainCar
from ..network.scanners import TrackObjectScanner
from ..network.scanners import Scanner
from .basemode import BaseMode


class AddTrainCarMode(BaseMode):
    name = "Add train car"

    def __init__(self, app):
        super().__init__(app)
        self.traincar_model = TrainCarBulk
        self.attach_length = 50

    def attach_traincar(self, traincar_scan, backwards):
        length_scan = Scanner(
            traincar_scan.final_object.parent_segment,
            traincar_scan.final_object.t,
            backwards,
            self.traincar_model.length/2 + self.attach_length + traincar_scan.final_object.model.length/2
        )

        TrainCar(
            self.app.trains,
            self.traincar_model,
            length_scan.final_segment,
            length_scan.final_t
        )

    def add_traincar(self, segment, t):

        traincar_scans = [
            TrackObjectScanner(segment, t, True, TrainCar),
            TrackObjectScanner(segment, t, False, TrainCar),
        ]

        for i, tcs in enumerate(traincar_scans):
            if tcs.final_object is not None:
                min_length = self.traincar_model.length/2 + self.attach_length + tcs.final_object.model.length/2
                if tcs.length_travelled < min_length:
                    other_tcs = traincar_scans[(i + 1)%2]
                    if other_tcs.final_object is not None:
                        other_min_length =\
                            self.traincar_model.length/2 + self.attach_length + other_tcs.final_object.model.length/2
                        if other_tcs.length_travelled < other_min_length:
                            print("Both too close")
                            return
                    print("One too close")
                    self.attach_traincar(tcs, i == 1)
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
