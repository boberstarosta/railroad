
from .. import geometry
from ..trains.models import *
from ..trains.traincar import TrainCar
from ..network.scanners import TrainCarScanner
from ..network.scanners import Scanner
from ..trains.coupling import Coupling
from .basemode import BaseMode


class AddTrainCarMode(BaseMode):
    name = "Add train car"

    def __init__(self, app):
        super().__init__(app)
        self.traincar_model = TrainCarBulk

    @staticmethod
    def get_traincars(segment, t):
        prev_traincar = TrainCarScanner(segment, t, backwards=True).traincar
        next_traincar = TrainCarScanner(segment, t, backwards=False).traincar
        traincars = [tc for tc in [prev_traincar, next_traincar] if tc is not None]
        return traincars

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_segment = self.app.network.get_nearest_track_segment(mouse, max_distance=self.search_radius)
            if nearest_segment is not None:
                t = geometry.nearest_t_on_line(mouse, nearest_segment.nodes[0].position,
                                               nearest_segment.nodes[1].position)
                traincars = self.get_traincars(nearest_segment, t)
                for tc in traincars:
                    distance = (tc.position - nearest_segment.position_from_t(t)).length
                    if distance < (tc.model.length + self.traincar_model.length) / 2:
                        nearest_coupling = self.app.trains.nearest_coupling(mouse, tc)
                        if len(nearest_coupling.traincars) < 2:
                            if nearest_coupling is tc.couplings[0]:
                                backwards = True
                            else:
                                backwards = False
                            track = Scanner(
                                tc.parent_segment, tc.t, backwards,
                                tc.model.length/2 + Coupling.length + self.traincar_model.length/2
                            )
                            if track.final_segment is not None:
                                new_traincar = TrainCar(
                                    self.app.trains, self.traincar_model,
                                    track.final_segment, track.final_t,
                                    coupling0=nearest_coupling
                                )
                        return
                TrainCar(
                    self.app.trains,
                    self.traincar_model,
                    nearest_segment, t
                )
