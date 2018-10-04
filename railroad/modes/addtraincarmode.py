
from .. import geometry
from ..trains.models import *
from ..trains.traincar import TrainCar
from ..trains.traincartrackfollower import TrainCarTrackFollower
from .basemode import BaseMode


class AddTrainCarMode(BaseMode):
    name = "Add train car"

    def __init__(self, app):
        super().__init__(app)
        self.traincar_model = TrainCarBulk

    def get_traincars(self, segment, t):
        prev_traincar = TrainCarTrackFollower(segment, t, backwards=True).traincar
        next_traincar = TrainCarTrackFollower(segment, t, backwards=False).traincar
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
                        return
                TrainCar(
                    self.app.trains,
                    self.traincar_model,
                    nearest_segment, t
                )
