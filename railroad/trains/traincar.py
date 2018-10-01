
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
        my_segment_length = self.segment.length
        if backwards:
            distance_to_node = my_segment_length * self.t
        else:
            distance_to_node = my_segment_length * (1 - self.t)

        if distance_to_node <= distance:
            # My segment is long enough
            delta_t = distance / my_segment_length
            new_t = self.t - delta_t if backwards else self.t + delta_t
            return self.segment, new_t
        else:
            # My segment is too short, start going further along the track
            my_position = self._position_from_t(self.segment, self.t)
            next_node = self.segment.nodes[0] if backwards else self.segment.nodes[1]
            current_segment = next_node.other_segment(self.segment)
            next_node = self.segment[0] if backwards else self.segment[1]
            while current_segment is not None:
                node_distances = [(n.position - my_position).length for n in current_segment.nodes]
                farthest_distance = max(node_distances)
                if farthest_distance >= distance:
                    # Some point on current_segment is distance away from my_position
                    # TODO: Find a point on <current_segment> whose distance to <my_position> is exactly <distance>
                    good_params = geometry.t_from_distance()
                    raise NotImplemented
                else:
                    # Both ends of current_segment are too close, continue to the next segment
                    current_segment = next_node.other_segment(current_segment)
                    next_node = current_segment.other_node(next_node)

            # Reached end of the line and still too close.
            # TODO: Do something if no point found
            raise NotImplemented

    def _get_wheel_points(self):
        segment0, t0 = self._follow_track(self.segment, self.t, self.model.wheelbase / 2, backwards=True)
        segment1, t1 = self._follow_track(self.segment, self.t, self.model.wheelbase / 2, backwards=False)
        return self._position_from_t(segment0, t0), self._position_from_t(segment1, t1)

    @staticmethod
    def _position_from_t(segment, t):
        vector = segment.nodes[1].position - segment.nodes[0].position
        return segment.nodes[0].position + vector * t

    def _update_sprite(self):
        wheel0, wheel1 = self._get_wheel_points()
        self.sprite.position = (wheel0 + wheel1) / 2
        self.sprite.rotation = -(self.segment.nodes[1].position - self.segment.nodes[0].position).angle

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        if value != self._t:
            self._t = value
            self._update_sprite()
