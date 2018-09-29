
import pyglet
from pyglet.gl import *
from .. import graphics
from .status import Status
from .panel import Panel


class Gui:
    def __init__(self, app):
        self.app = app
        self.batch = pyglet.graphics.Batch()
        self.notification_timer = 0
        self.notification = None
        self.status = Status(self)
        self.panel = Panel(self)
        self.app.window.push_handlers(self)

    def show_notification(self, text, time=2):
        if self.notification is not None:
            self.notification.delete()
        self.notification = pyglet.text.Label(
            text, font_size=24, bold=True, color=(255, 255, 255, 100),
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
        self.status.update(dt)
        self.panel.update(dt)

    def draw(self):
        self.batch.draw()
