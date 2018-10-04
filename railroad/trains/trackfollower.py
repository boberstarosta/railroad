
from ..network.basetrackfollower import BaseTrackFollower


class TrackFollower(BaseTrackFollower):
    """ Follows track for a given length """

    def __init__(self, segment, t, backwards, length):
        self.target_length = length
        self.length_travelled = 0
        self.final_segment = None
        self.final_t = None
        self.run(segment, t, backwards)

    def check_segment(self, current_segment, node, min_t, max_t):
        remaining_length = self.target_length - self.length_travelled
        segment_length = current_segment.length
        possible_length = (max_t - min_t) * segment_length
        if possible_length >= remaining_length:
            self.final_segment = current_segment
            if node is current_segment.nodes[0]:
                self.final_t = min_t + (remaining_length / segment_length)
            else:
                self.final_t = max_t - (remaining_length / segment_length)
            return True
