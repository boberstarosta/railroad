
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
        traincars = [tc for tc in segment.traincars if t_interval[0] < tc < t_interval[1]]
        if len(traincars) > 0:
            return traincars[0]

        node = segment.nodes[0] if backwards else segment.nodes[1]
        current_segment = node.other_segment(segment)
        next_node = None if current_segment is None else current_segment.other_node(node)

        while current_segment is not None:
            if len(current_segment.traincars) > 0:
                sorted_traincars = sorted(current_segment.traincars, key=lambda tc: tc.t)
                if next_node is current_segment.nodes[0]:
                    return sorted_traincars[0]
                else:
                    return sorted_traincars[-1]
            current_segment = next_node.other_segment(current_segment)
            if current_segment is not None:
                next_node = current_segment.other_node(next_node)

        return None

    def get_nearest_traincar(self, segment, t):
        prev_traincar = self.follow_track_until_traincar(segment, t, backwards=True)
        next_traincar = self.follow_track_until_traincar(segment, t, backwards=False)
        traincars = [tc for tc in [prev_traincar, next_traincar] if tc is not None]
        nearest_tc = None
        if len(traincars) == 1:
            nearest_tc = traincars[0]
        elif len(traincars) >= 2:
            def distance(segment, t, traincar):
                position = TrainCar._position_from_t(segment, t)
                return (traincar.position - position).length
            nearest_tc = min(traincars, key=lambda tc: distance(segment, t, tc))
        return nearest_tc

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_segment = self.app.network.get_nearest_track_segment(mouse, max_distance=self.search_radius)
            if nearest_segment is not None:
                t = geometry.nearest_t_on_line(mouse, nearest_segment.nodes[0].position,
                                               nearest_segment.nodes[1].position)
                nearest_tc = self.get_nearest_traincar(nearest_segment, t)
                TrainCar(
                    self.app.trains,
                    self.traincar_model,
                    nearest_segment, t
                )
