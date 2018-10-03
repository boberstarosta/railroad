
from enum import Enum
from .signal import Signal
from .blocksignal import BlockSignal


class TrackStatus(Enum):

    dead_end = 1
    wrong_junction = 2
    junction_turn = 3


class FollowResult:

    def __init__(self, start_segment, start_t):
        self.start_segment = start_segment
        self.start_t = start_t
        self.visited_segments = []
        self.loop = False
        self.dead_end = False
        self.wrong_junction = False
        self.junction_turns = []
        self.track_objects = []
        self.traincars = []
        self.elapsed_distance = 0.0

        self.next_signal_types = [Signal, BlockSignal]

    @property
    def first_signal(self):
        signals = [to for to in self.track_objects if type(to) in self.next_signal_types]
        return None if len(signals) == 0 else signals[0]

    @property
    def first_traincar(self):
        return None if len(self.traincars) == 0 else self.traincars[0]

    @property
    def traincar_present_before_signal(self):
        if len(self.traincars) > 0:
            if self.first_signal is None:
                return self.first_traincar is not None
        else:
            return False


def stripped_sorted_by_t(segment, next_node, collection, min_t, max_t):
    stripped_by_t = [x for x in collection if min_t <= x.t <= max_t]
    reverse = next_node is segment.nodes[0]
    return sorted(stripped_by_t, key=lambda x: x.t, reverse=reverse)

def check_junctions(segment, next_node, result):
    if segment is next_node.turn:
        if not next_node.is_switched:
            result.wrong_junction = True
        result.junction_turns.append(next_node)
    elif segment is next_node.point:
        if next_node.is_switched:
            result.junction_turns.append(next_node)
    elif next_node.is_switched:  # segment is next_node.straight
        result.wrong_junction = True


def follow_track(segment, t, backwards, break_func, result=None):
    if result is None:
        result = FollowResult(segment, t)

    if segment in result.visited_segments:
        result.loop = True
        return result

    result.visited_segments.append(segment)

    if backwards:
        next_node = segment.nodes[0]
        segment_distance = t*segment.length
        t_constraints = (t, 1)
    else:
        next_node = segment.nodes[1]
        segment_distance = (1 - t)*segment.length
        t_constraints = (0, t)

    result.elapsed_distance += segment_distance

    result.traincars.extend(stripped_sorted_by_t(segment.traincars, *t_constraints))
    result.track_objects.extend(stripped_sorted_by_t(segment.track_objects, *t_constraints))

    next_segment = next_node.other_segment(segment)

    if next_segment is None:
        result.dead_end = True
        return result

    # Next segment exists
    if len(next_node.edges) == 3:
        check_junctions(segment, next_node, result)

    if break_func(segment, t, backwards, result):
        return result

    # Proceed to the next segment
    if next_node is next_segment.nodes[0]:
        next_t = 0
        next_backwards = False
    else:
        next_t = 1
        next_backwards = True

    return follow_track(next_segment, next_t, next_backwards, break_func, result)
