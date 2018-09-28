from .basesignal import BaseSignal
from .signal import Signal
from .. import graphics


class DistantSignal(BaseSignal):
    
    height = 300
    corona_height = 70
    corona_start = 80
    corona_spacing = 49.5
    
    image = graphics.img.distant_signal
    corona_images = [
        graphics.img.corona_green,
        graphics.img.corona_orange,
    ]
    
    def __init__(self, network, parent_segment, t):
        super().__init__(network, parent_segment, t)
    
    def check_track_ahead(self):
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
        
        while current_segment is not None and current_segment not in checked_segments:
            
            # Check for nearest signals
            nearest_signal = current_segment.nearest_track_object(Signal, node, min_t=min_t, max_t=max_t)
            if nearest_signal is not None:
                return nearest_signal.setting
            
            # Check for junctions
            next_node = current_segment.other_node(node)
            if len(next_node.edges) == 3:
                if ((next_node.is_switched and current_segment is next_node.straight)
                or (not next_node.is_switched and current_segment is next_node.turn)):
                    return "off"
            
            # Proceed to next segment
            checked_segments.append(current_segment)
            node = current_segment.other_node(node)
            current_segment = node.other_segment(current_segment)
            # Only needed for self.parent_segment, no longer needed now
            min_t = None
            max_t = None
        
        return "off"
    
    def update_setting(self):
        next_setting = self.check_track_ahead()
        self.change_setting(next_setting)
    
    def change_setting(self, next_setting):
        settings_dic = {
            "off":  [0, 0],
            "full": [1, 0],
            "40":   [0, 2],
            "stop": [0, 1],
        }
        self.light_states = settings_dic[next_setting]

