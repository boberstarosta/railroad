
import pyglet
from pyglet.window import key
from .. import graphics
from ..network.signal import Signal
from ..network.distantsignal import DistantSignal
from ..network.opentrackmarker import OpenTrackMarker
from .radiogroup import RadioGroup


class TrackObjectSelect(RadioGroup):

    def __init__(self, gui, align_x, align_y, padding=10):
        self.object_data = [
            (key.S, Signal),
            (key.N, DistantSignal),
            (key.O, OpenTrackMarker),
        ]
        data = [(k, oc.__name__) for k, oc in self.object_data]
        super().__init__(gui, data, align_x, align_y, padding)
    
    def on_index_changed(self, value):
        self.gui.app.mode.track_object_class = self.object_data[value][1]

