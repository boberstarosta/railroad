
from .. import graphics
from .basesignal import BaseSignal
from .trackahead import TrackAhead


class BlockSignal(BaseSignal):

    height = 300
    corona_height = 70
    corona_start = 32
    corona_spacing = 49.5

    image = graphics.img.block_signal
    corona_images = [
        graphics.img.corona_green,
        graphics.img.corona_red,
        graphics.img.corona_orange,
    ]

    def __init__(self, network, parent_segment, t, rotated=False):
        super().__init__(network, parent_segment, t, rotated)
        self.setting = "full"

    class TrackAhead:
        def __init__(self, next_signal, junction_turn, junction_wrong, open_track):
            self.next_signal = next_signal
            self.junction_turn = junction_turn
            self.junction_wrong = junction_wrong
            self.open_track = open_track

    def update_setting(self):
        setting = "full"
        next_setting = "full"
        track_ahead = TrackAhead(self)
        if track_ahead.junction_wrong or track_ahead.traincar_present:
            setting = "stop"
        else:
            if track_ahead.next_signal is None:
                if not track_ahead.open_track:
                    setting = "stop"
            else:
                next_setting = track_ahead.next_signal.setting
        self.change_setting(setting, next_setting)

    def change_setting(self, setting, next_setting):
        self.setting = setting
        settings_dic = {
            ("full", "full"): [1, 0, 0],
            ("full", "40"):   [0, 0, 2],
            ("full", "stop"): [0, 0, 1],
            ("stop", "full"): [0, 1, 0],
            ("stop", "40"):   [0, 1, 0],
            ("stop", "stop"): [0, 1, 0],
        }
        self.light_states = settings_dic[setting, next_setting]
