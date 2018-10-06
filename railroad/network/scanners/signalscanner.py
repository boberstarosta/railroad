
from .basescanner import BaseScanner
import railroad.trains.traincar
import railroad.network.signals.signal
import railroad.network.signals.blocksignal
import railroad.network.signals.distantsignal
import railroad.network.opentrackmarker


class SignalScanner(BaseScanner):

    def __init__(self, caller):
        self.caller = caller

        self.next_signal = None
        self.junction_wrong = False
        self.junction_turn = False
        self.open_track = False
        self.traincar_present = False

        self.run(caller.parent_segment, caller.t, caller.rotated)

    def check_segment(self, current_segment, node, min_t, max_t):
            # Always check for signals and open track markers
            to_classes = [
                railroad.network.signals.signal.Signal,
                railroad.network.signals.blocksignal.BlockSignal,
                railroad.network.opentrackmarker.OpenTrackMarker,
            ]

            # Check for traincars only if caller is not a DistantSignal
            if not isinstance(self.caller, railroad.network.signals.distantsignal.DistantSignal):
                to_classes.append(railroad.trains.traincar.TrainCar)

            nearest_track_object = current_segment.nearest_track_object(
                node, *to_classes,
                min_t=min_t, max_t=max_t, exclude=[self.caller]
            )

            # Return with a status depending on nearest_track_object type
            if isinstance(nearest_track_object, railroad.trains.traincar.TrainCar):
                self.traincar_present = True
                return True
            elif isinstance(nearest_track_object, railroad.network.opentrackmarker.OpenTrackMarker):
                self.open_track = True
                return True
            elif isinstance(nearest_track_object, railroad.network.signals.signal.Signal) \
                    or isinstance(nearest_track_object, railroad.network.signals.blocksignal.BlockSignal):
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
