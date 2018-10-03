
from .. import geometry
from ..trains.models import *
from ..trains.traincar import TrainCar
from .basemode import BaseMode


class AddTrainCarMode(BaseMode):
    name = "Add train car"

    def __init__(self, app):
        super().__init__(app)
        self.traincar_model = TrainCarBulk

    def follow_track_until_traincar(self, segment, t, backwards):
        t_interval = (0, t) if backwards else (t, 1)
        traincars = [tc for tc in segment.traincars if t_interval[0] < tc.t < t_interval[1]]
        if len(traincars) > 0:
            sorted_by_delta_t = sorted(traincars, key=lambda tc: abs(t - tc.t))
            return sorted_by_delta_t[0]

        node = segment.nodes[0] if backwards else segment.nodes[1]
        current_segment = node.other_segment(segment)
        next_node = None if current_segment is None else current_segment.other_node(node)

        while current_segment is not None:
            if len(current_segment.traincars) > 0:
                sorted_traincars = sorted(current_segment.traincars, key=lambda tc: tc.t)
                if next_node is current_segment.nodes[0]:
                    return sorted_traincars[-1]
                else:
                    return sorted_traincars[0]
            current_segment = next_node.other_segment(current_segment)
            if current_segment is not None:
                next_node = current_segment.other_node(next_node)

        return None

    def get_traincars(self, segment, t):
        prev_traincar = self.follow_track_until_traincar(segment, t, backwards=True)
        next_traincar = self.follow_track_until_traincar(segment, t, backwards=False)
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
                print(traincars)
                for tc in traincars:
                    distance = (tc.position - TrainCar.position_from_t(nearest_segment, t)).length
                    print(id(tc), distance, (tc.model.length + self.traincar_model.length) / 2)
                    if distance < (tc.model.length + self.traincar_model.length) / 2:
                        return
                TrainCar(
                    self.app.trains,
                    self.traincar_model,
                    nearest_segment, t
                )
