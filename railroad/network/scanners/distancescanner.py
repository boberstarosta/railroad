
from railroad import geometry
from .basescanner import BaseScanner


class DistanceScanner(BaseScanner):
    """Follows a track for a given distance.
        Can be used to get track a point on a track that is a given distance away from traincar. 
    """

    def __init__(self, traincar, backwards):
        self.start_position = traincar.parent_segment.position_from_t(traincar.t)
        self.target_distance = traincar.model.wheelbase / 2

        self.final_segment = traincar.parent_segment

        delta_t = self.target_distance / traincar.parent_segment.length
        if backwards:
            delta_t *= -1
        self.final_t = traincar.t + delta_t

        self.run(traincar.parent_segment, traincar.t, backwards)

    def check_segment(self, current_segment, node, min_t, max_t):
        params = geometry.param_from_distance(
            self.start_position,
            current_segment.nodes[0].position,
            current_segment.nodes[1].position - current_segment.nodes[0].position,
            self.target_distance
        )
        good_params = [p for p in params if min_t < p < max_t]
        if len(good_params) == 1:
            # One param is within current_segment
            self.final_segment = current_segment
            self.final_t = good_params[0]
            return True
        elif len(good_params) == 2:
            # Two params are within current_segment
            self.final_segment = current_segment
            # Choose the param closer to node (closer to where I'm coming from)
            t = max(good_params) if node is current_segment.nodes[1] else min(good_params)
            return current_segment, t
