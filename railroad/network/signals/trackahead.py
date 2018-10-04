
from railroad.network.opentrackmarker import OpenTrackMarker
from ...trains.traincar import TrainCar


class TrackAhead:
    def __init__(self, caller):
        from railroad.network.signals.signal import Signal
        from railroad.network.signals.blocksignal import BlockSignal

        self.next_signal = None
        self.junction_wrong = False
        self.junction_turn = False
        self.open_track = False
        self.traincar_present = False

        checked_segments = []

        node_index = 1 if caller.rotated else 0
        node = caller.parent_segment.nodes[node_index]
        current_segment = caller.parent_segment

        if caller.rotated:
            min_t = 0.0
            max_t = caller.t
        else:
            min_t = caller.t
            max_t = 1.0

        while self.next_signal is None and current_segment is not None and \
                current_segment not in checked_segments:

            # Check for both traincars and signals
            nearest_track_object = current_segment.nearest_track_object(
                node, TrainCar, Signal, BlockSignal, OpenTrackMarker, min_t=min_t, max_t=max_t, exclude=[caller])

            # Return with a status depending on nearest_track_object type
            if isinstance(nearest_track_object, TrainCar):
                self.traincar_present = True
                return
            elif isinstance(nearest_track_object, OpenTrackMarker):
                self.open_track = True
                return
            elif isinstance(nearest_track_object, Signal) or isinstance(nearest_track_object, BlockSignal):
                self.next_signal = nearest_track_object
                return

            # Check for junctions
            next_node = current_segment.other_node(node)
            if len(next_node.edges) == 3:
                if ((next_node.is_switched and current_segment is next_node.straight)
                        or (not next_node.is_switched and current_segment is next_node.turn)):
                    self.junction_wrong = True
                    return
                else:
                    junction_turn = (
                            (current_segment is next_node.turn) or
                            (current_segment is next_node.point and next_node.is_switched)
                    )
                    if junction_turn:
                        self.junction_turn = True

            # Proceed to next segment
            checked_segments.append(current_segment)
            node = current_segment.other_node(node)
            current_segment = node.other_segment(current_segment)

            # Only needed for self.parent_segment, no longer needed now
            min_t = 0.0
            max_t = 1.0
