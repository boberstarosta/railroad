
from .. import geometry


class TrainCar:

    def __init__(self, trains, model, segment, t, rotated=False, parent_consist=None):
        self.trains = trains
        self.model = model
        self.segment = segment
        self._t = t
        self._rotated = rotated
        self._position = None
        self.parent_consist = parent_consist
        self.sprite = model.create_sprite(trains.network.app.batch)
        trains.traincars.append(self)
        segment.traincars.append(self)
        self._update_sprite()

    def delete(self):
        self.sprite.delete()
        self.trains.traincars.remove(self)
        self.segment.traincars.remove(self)

    def update(self, dt):
        pass

    def _follow_track_dist(self, distance, backwards):
        # First check if my segment is long enough
        delta_t = distance / self.segment.length
        if backwards:
            delta_t *= -1
        new_t = self.t + delta_t

        if 0 < new_t < 1:
            # My segment is long enough
            return self.segment, new_t
        else:
            # My segment is too short, start going further along the track
            my_position = self.position_from_t(self.segment, self.t)
            next_node = self.segment.nodes[0] if backwards else self.segment.nodes[1]
            current_segment = next_node.other_segment(self.segment)
            if current_segment is not None:
                next_node = current_segment.other_node(next_node)
                while current_segment is not None:
                    params = geometry.t_from_distance(
                        my_position,
                        current_segment.nodes[0].position,
                        current_segment.nodes[1].position - current_segment.nodes[0].position,
                        distance
                    )
                    good_params = [p for p in params if 0 < p < 1]
                    if len(good_params) == 1:
                        # One param is within current_segment
                        return current_segment, good_params[0]
                    elif len(good_params) == 2:
                        # Two params are within current_segment
                        # Choose the param further from next_node (closer to my segment)
                        t = max(good_params) if next_node is current_segment.nodes[0] else min(good_params)
                        return current_segment, t
                    else:
                        # Both ends of current_segment are too close, continue to the next segment
                        current_segment = next_node.other_segment(current_segment)
                        if current_segment is not None:
                            next_node = current_segment.other_node(next_node)

            # Reached end of the line and still too close.
            # TODO: Do something if no point found
            return self.segment, new_t

    def _get_wheel_points(self):
        segment0, t0 = self._follow_track_dist(self.model.wheelbase / 2, backwards=True)
        segment1, t1 = self._follow_track_dist(self.model.wheelbase / 2, backwards=False)
        return self.position_from_t(segment0, t0), self.position_from_t(segment1, t1)

    @staticmethod
    def position_from_t(segment, t):
        vector = segment.nodes[1].position - segment.nodes[0].position
        return segment.nodes[0].position + vector * t

    def _update_sprite(self):
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
            self._update_sprite()

    @property
    def position(self):
        return self._position
