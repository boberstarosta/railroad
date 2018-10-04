
from ... import graphics
from .basesignal import BaseSignal
import railroad.network.signals.signaltrackfollower


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
    
    def __init__(self, network, parent_segment, t, rotated=False):
        super().__init__(network, parent_segment, t, rotated)
        self.setting = "stop"
    
    def update_setting(self):
        # Default is "stop", "stop"
        setting = "stop"
        next_setting = "stop"
        track_ahead = railroad.network.signals.signaltrackfollower.SignalTrackFollower(self)
        if not track_ahead.junction_wrong and not track_ahead.traincar_present:
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
