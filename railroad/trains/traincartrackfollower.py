
from ..network.basetrackfollower import BaseTrackFollower
from .traincar import TrainCar


class TrainCarTrackFollower(BaseTrackFollower):
    """Follows track until a traincar is found"""

    def __init__(self, segment, t, backwards):
        self.traincar = None
        self.run(segment, t, backwards)

    def check_segment(self, current_segment, node, min_t, max_t):
        self.traincar = current_segment.nearest_track_object(node, TrainCar, min_t, max_t)
        if self.traincar is not None:
            return True
