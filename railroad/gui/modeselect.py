
from pyglet.window import key
from ..modes import *
from .radiogroup import RadioGroup


class ModeSelect(RadioGroup):

    def __init__(self, gui, align_x, align_y, padding=10):
        self.mode_data = [
            (key.A, AddTrackMode),
            (key.M, MoveTrackMode),
            (key.D, DeleteTrackMode),
            (key.I, InsertNodeMode),
            (key.X, RemoveNodeMode),
            (key.B, StraightenTrackMode),
            (key.J, SwitchJunctionMode),
            (key.K, AddTrackObjectMode),
            (key.R, RotateTrackObjectMode),
            (key.L, RemoveTrackObjectMode),
            (key.SEMICOLON, MoveTrackObjectMode),
            (key.E, AddSceneryObjectMode),
        ]
        data = [(k, mc.name) for k, mc in self.mode_data]
        super().__init__(gui, data, align_x, align_y, padding)
    
    def on_index_changed(self, value):
        self.gui.app.change_mode(self.mode_data[value][1])
