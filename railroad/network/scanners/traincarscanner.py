
from .basescanner import BaseScanner
import railroad.trains.traincar


class TrainCarScanner(BaseScanner):
    """Follows track until first traincar is found"""

    def __init__(self, segment, t, backwards):
        self.traincar = None
        self.run(segment, t, backwards)

    def check_segment(self, current_segment, node, min_t, max_t):
        self.traincar = current_segment.nearest_track_object(node, railroad.trains.traincar.TrainCar, min_t, max_t)
        if self.traincar is not None:
            return True
