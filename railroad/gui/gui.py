
import pyglet
from pyglet.gl import *
from .. import graphics
from .. import modes
from .button import ChangeModeButton


class Gui:
    def __init__(self, app):
        self.app = app
        self.batch = pyglet.graphics.Batch()
        self._create_buttons()

    def _create_buttons(self, padding=10):
        button_args_list = [
            (graphics.img.button_add_track,       modes.AddTrackMode),
            (graphics.img.button_move_track,      modes.MoveTrackMode),
            (graphics.img.button_delete_track,    modes.DeleteTrackMode),
            (graphics.img.button_insert_node,     modes.InsertNodeMode),
            (graphics.img.button_remove_node,     modes.RemoveNodeMode),
            (graphics.img.button_switch_junction, modes.SwitchJunctionMode),
        ]
        width = len(button_args_list)*ChangeModeButton.image_back.width + (len(button_args_list) - 1)*padding
        x = self.app.window.width // 2 - width // 2
        y = ChangeModeButton.image_back.height // 2 + padding
        for args in button_args_list:
            ChangeModeButton(self, *args, x=x, y=y)
            x += ChangeModeButton.image_back.width + padding

    def update(self, dt):
        pass

    def draw(self):
        self.batch.draw()
