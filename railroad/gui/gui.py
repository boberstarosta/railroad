
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
        self.notification_timer = 0
        self.notification = None

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

    def show_notification(self, text, time=2):
        if self.notification is not None:
            self.notification.delete()
        self.notification = pyglet.text.Label(
            text, font_size=24, bold=True, color=(255, 255, 255, 127),
            x=self.app.window.width//2, y=self.app.window.height//2,
            width=self.app.window.width,
            anchor_x="center", anchor_y="center", align="center", multiline=True,
            batch=self.batch, group=graphics.group.gui_front
        )
        self.notification_timer = time

    def update(self, dt):
        if self.notification is not None:
            self.notification_timer -= dt
            if self.notification_timer <= 0:
                self.notification.delete()

    def draw(self):
        self.batch.draw()
