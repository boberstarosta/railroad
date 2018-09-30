
from .. import graphics
from .basesignal import BaseSignal
from .trackahead import TrackAhead


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
    
    def __init__(self, network, parent_segment, t, rotated=False):
        super().__init__(network, parent_segment, t, rotated)
    
    def update_setting(self):
        next_setting = "off"
        track_ahead = TrackAhead(self)
        if track_ahead.next_signal is not None:
            next_setting = track_ahead.next_signal.setting

        self.change_setting(next_setting)
    
    def change_setting(self, next_setting):
        settings_dic = {
            "off":  [0, 0],
            "full": [1, 0],
            "40":   [0, 2],
            "stop": [0, 1],
        }
        self.light_states = settings_dic[next_setting]

