"""
BaseTrackScanner

    Inherit from this class and override check_segment method to follow a track.
    Call run() method to start following.
"""

class BaseScanner:

    def run(self, segment, t, backwards):
        checked_segments = []

        node = segment.nodes[1 if backwards else 0]
        current_segment = segment

        if backwards:
            min_t = 0.0
            max_t = t
        else:
            min_t = t
            max_t = 1.0

        while current_segment is not None and current_segment not in checked_segments:
            if self.check_segment(current_segment, node, min_t, max_t):
                return

            # Proceed to next segment
            checked_segments.append(current_segment)
            node = current_segment.other_node(node)
            current_segment = node.other_segment(current_segment)

            # Only needed for the first segment, no longer needed now
            min_t = 0.0
            max_t = 1.0

    def check_segment(self, current_segment, node, min_t, max_t):
        """ Override this method. Return True to stop following """
        pass
