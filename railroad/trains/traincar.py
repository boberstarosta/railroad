
from .. import geometry


class TrainCar:

    def __init__(self, trains, model, segment, t, rotated=False, parent_consist=None):
        self.trains = trains
        self.model = model
        self.segment = segment
        self._t = t
        self._rotated = rotated
        self.parent_consist = parent_consist
        self.sprite = model.create_sprite(trains.network.app.batch)
        trains.traincars.append(self)
        self._update_sprite()

    def delete(self):
        self.sprite.delete()
        self.trains.traincars.remove(self)

    def update(self, dt):
        pass

    @classmethod
    def _follow_track(cls, segment, t, distance, backwards):
        current_segment_length = segment.length
        if backwards:
            distance_to_node = current_segment_length * t
        else:
            distance_to_node = current_segment_length * (1 - t)

        if distance_to_node > distance:
            delta_t = distance / current_segment_length
            new_t = t - delta_t if backwards else t + delta_t
            return segment, new_t
        else:
            approaching_node = segment.nodes[0] if backwards else segment.nodes[1]
            next_segment = approaching_node.other_segment(segment)
            if next_segment is None:
                print("End of line.", distance_to_node, backwards)
                return segment, t
            next_distance = distance - distance_to_node
            next_backwards = approaching_node is next_segment.nodes[1]
            next_t = 1.0 if next_backwards else 0.0
            return cls._follow_track(next_segment, next_t, next_distance, next_backwards)

    def _follow_track_dist(self, distance, backwards):
        # First check if my current node is long enough
        delta_t = distance / self.segment.length
        new_t = self.t - delta_t if backwards else self.t + delta_t

        if 0 < new_t < 1:
            # My segment is long enough
            return self.segment, new_t
        else:
            print("following", distance, backwards)
            # My segment is too short, start going further along the track
            my_position = self._position_from_t(self.segment, self.t)
            next_node = self.segment.nodes[0] if backwards else self.segment.nodes[1]
            current_segment = next_node.other_segment(self.segment)
            while current_segment is not None:
                params = geometry.t_from_distance(
                    my_position,
                    current_segment.nodes[0].position,
                    current_segment.nodes[1].position - current_segment.nodes[0].position,
                    distance
                )
                if True in [0 < p < 1 for p in params]:
                    # At least one param is within current_segment
                    if len(params) == 1:
                        return current_segment, params[0]
                    elif len(params) == 2:
                        t = max(params) if backwards else min(params)
                        return current_segment, t
                else:
                    # Both ends of current_segment are too close, continue to the next segment
                    current_segment = next_node.other_segment(current_segment)
                    if current_segment is not None:
                        next_node = current_segment.other_node(next_node)

            # Reached end of the line and still too close.
            # TODO: Do something if no point found
            print("End of line", distance, backwards)
            return self.segment, new_t

    def _get_wheel_points(self):
        segment0, t0 = self._follow_track_dist(self.model.wheelbase / 2, backwards=True)
        segment1, t1 = self._follow_track_dist(self.model.wheelbase / 2, backwards=False)
        return self._position_from_t(segment0, t0), self._position_from_t(segment1, t1)

    @staticmethod
    def _position_from_t(segment, t):
        vector = segment.nodes[1].position - segment.nodes[0].position
        return segment.nodes[0].position + vector * t

    def _update_sprite(self):
        wheel0, wheel1 = self._get_wheel_points()
        self.sprite.position = (wheel0 + wheel1) / 2
        self.sprite.rotation = -(wheel1 - wheel0).angle

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        if value != self._t:
            self._t = value
            self._update_sprite()
