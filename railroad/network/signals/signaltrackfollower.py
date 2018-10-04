
from ..basetrackfollower import BaseTrackFollower
from ..opentrackmarker import OpenTrackMarker
from ...trains.traincar import TrainCar
from .signal import Signal
from .blocksignal import BlockSignal


class SignalTrackFollower(BaseTrackFollower):

    def __init__(self, caller):
        self.caller = caller

        self.next_signal = None
        self.junction_wrong = False
        self.junction_turn = False
        self.open_track = False
        self.traincar_present = False

        super().__init__(caller.parent_segment, caller.t, caller.rotated)

    def check_segment(self, current_segment, node, min_t, max_t):
            # Check for both traincars and signals
            nearest_track_object = current_segment.nearest_track_object(
                node, TrainCar, Signal, BlockSignal, OpenTrackMarker, min_t=min_t, max_t=max_t, exclude=[self.caller])

            # Return with a status depending on nearest_track_object type
            if isinstance(nearest_track_object, TrainCar):
                self.traincar_present = True
                return True
            elif isinstance(nearest_track_object, OpenTrackMarker):
                self.open_track = True
                return True
            elif isinstance(nearest_track_object, Signal) or isinstance(nearest_track_object, BlockSignal):
                self.next_signal = nearest_track_object
                return True

            # Check for junctions
            next_node = current_segment.other_node(node)
            if len(next_node.edges) == 3:
                if ((next_node.is_switched and current_segment is next_node.straight)
                        or (not next_node.is_switched and current_segment is next_node.turn)):
                    self.junction_wrong = True
                    return True
                else:
                    junction_turn = (
                            (current_segment is next_node.turn) or
                            (current_segment is next_node.point and next_node.is_switched)
                    )
                    if junction_turn:
                        self.junction_turn = True
