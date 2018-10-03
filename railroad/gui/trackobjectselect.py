
from pyglet.window import key
from railroad.network.signals.signal import Signal
from railroad.network.signals.distantsignal import DistantSignal
from railroad.network.signals.blocksignal import BlockSignal
from ..network.opentrackmarker import OpenTrackMarker
from .radiogroup import RadioGroup


class TrackObjectSelect(RadioGroup):

    def __init__(self, gui, align_x, align_y, padding=10):
        self.object_data = [
            (key.S, Signal),
            (key.C, BlockSignal),
            (key.N, DistantSignal),
            (key.O, OpenTrackMarker),
        ]
        data = [(k, oc.__name__) for k, oc in self.object_data]
        super().__init__(gui, data, align_x, align_y, padding)
    
    def on_index_changed(self, value):
        self.gui.app.mode.track_object_class = self.object_data[value][1]
        self.gui.show_notification("Track object: {}".format(self.selected_class.__name__))

    @property
    def selected_class(self):
        return self.object_data[self.index][1]
