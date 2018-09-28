from .basesignal import BaseSignal
from .opentrackmarker import OpenTrackMarker
from .. import graphics


class Signal(BaseSignal):
    
    height = 300
    corona_height = 70
    corona_start = 32
    corona_spacing = 49.5
    
    image = graphics.img.signal
    corona_images = [
        graphics.img.corona_green,
        graphics.img.corona_orange,
        graphics.img.corona_red,
        graphics.img.corona_orange,
        graphics.img.corona_white,
    ]
    
    def __init__(self, network, parent_segment, t):
        super().__init__(network, parent_segment, t)
        self.setting = "stop"
    
    class TrackAhead:
        def __init__(self, next_signal, junction_turn, junction_wrong, open_track):
            self.next_signal = next_signal
            self.junction_turn = junction_turn
            self.junction_wrong = junction_wrong
            self.open_track = open_track
    
    def check_track_ahead(self):
        track_ahead = self.TrackAhead(None, False, False, False)
        checked_segments = []
        
        node_index = 1 if self.rotated else 0
        node = self.parent_segment.nodes[node_index]
        current_segment = self.parent_segment
        
        if self.rotated:
            min_t = None
            max_t = self.t
        else:
            min_t = self.t
            max_t = None
        exclude = [self]
        
        while track_ahead.next_signal is None and current_segment is not None and current_segment not in checked_segments:
            
            nearest_open_track = current_segment.nearest_track_object(OpenTrackMarker, node, min_t=min_t, max_t=max_t)
            if nearest_open_track is not None:
                track_ahead.open_track = True
                return track_ahead

            # Check for nearest signals
            nearest_signal = current_segment.nearest_track_object(type(self), node, min_t=min_t, max_t=max_t, exclude=exclude)
            if nearest_signal is not None:
                track_ahead.next_signal = nearest_signal
                return track_ahead
            
            # Check for junctions
            next_node = current_segment.other_node(node)
            if len(next_node.edges) == 3:
                if ((next_node.is_switched and current_segment is next_node.straight)
                or (not next_node.is_switched and current_segment is next_node.turn)):
                    track_ahead.junction_wrong = True
                else:
                    junction_turn = (
                        (current_segment is next_node.turn) or
                        (current_segment is next_node.point and next_node.is_switched)
                    )
                    if junction_turn:
                        track_ahead.junction_turn = True
                
            # Proceed to next segment
            checked_segments.append(current_segment)
            node = current_segment.other_node(node)
            current_segment = node.other_segment(current_segment)
            # Only needed for self.parent_segment, no longer needed now
            min_t = None
            max_t = None
            exclude = []
                
        return track_ahead
    
    def update_setting(self):
        # Default is "stop", "stop"
        setting = "stop"
        next_setting = "stop"
        track_ahead = self.check_track_ahead()
        if not track_ahead.junction_wrong:  # If junction_wrong, leave default stop stop
            if track_ahead.junction_turn:
                setting = "40"
            else:
                setting = "full"
            if track_ahead.next_signal is None:
                if track_ahead.open_track:
                    next_setting = "full"
                else:
                    setting = "stop"
            else:
                next_setting = track_ahead.next_signal.setting
        self.change_setting(setting, next_setting)
    
    def change_setting(self, setting, next_setting):
        self.setting = setting
        settings_dic = {
            ("full", "full"): [1, 0, 0, 0, 0],
            ("full", "40"):   [0, 2, 0, 0, 0],
            ("full", "stop"): [0, 1, 0, 0, 0],
            ("40", "full"):   [1, 0, 0, 1, 0],
            ("40", "40"):     [0, 2, 0, 1, 0],
            ("40", "stop"):   [0, 1, 0, 1, 0],
            ("stop", "full"): [0, 0, 1, 0, 0],
            ("stop", "40"):   [0, 0, 1, 0, 0],
            ("stop", "stop"): [0, 0, 1, 0, 0],
        }
        self.light_states = settings_dic[setting, next_setting]

