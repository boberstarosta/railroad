
from .. import geometry
from ..trains.models import *
from ..trains.traincar import TrainCar
from ..trains.wheel import Wheel
from ..network.scanners import TrackObjectScanner
from ..network.scanners import Scanner
from .basemode import BaseMode


class AddTrainCarMode(BaseMode):
    name = "Add train car"

    def __init__(self, app):
        super().__init__(app)
        self.traincar_model = TrainCarBulk

    def add_traincar(self, segment, t):

        traincar_scans = [
            TrackObjectScanner(segment, t, True, TrainCar),
            TrackObjectScanner(segment, t, False, TrainCar),
        ]

        for tcs in traincar_scans:
            if tcs.final_object is not None:
                min_length = self.traincar_model.length/2 + 50 + tcs.final_object.model.length/2
                if tcs.length_travelled < min_length:
                    print("Too close")
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
