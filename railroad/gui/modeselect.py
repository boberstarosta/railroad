
import pyglet
from pyglet.window import key
from .. import graphics
from .. import geometry
from ..modes import *


class ModeSelect:

    mode_data = [
        (key.A, AddTrackMode),
        (key.M, MoveTrackMode),
        (key.D, DeleteTrackMode),
        (key.I, InsertNodeMode),
        (key.X, RemoveNodeMode),
        (key.B, StraightenTrackMode),
        (key.J, SwitchJunctionMode),
        (key.O, AddTrackObjectMode),
        (key.R, RotateTrackObjectMode),
    ]

    def __init__(self, gui, padding=10):
        self.gui = gui
        self._index = 0
        self.padding = padding

        self.check_sprite = pyglet.sprite.Sprite(graphics.img.gui_radio_check,
                                                 batch=gui.batch,
                                                 group=graphics.group.gui_front)
        self.check_sprite.scale = 0.75
        self.sprites = []
        self.labels = []

        for symbol, mode_class in self.mode_data:
            text = "[{}] ".format(key.symbol_string(symbol))
            text += mode_class.__name__ if mode_class.name is None else mode_class.name
            sprite = pyglet.sprite.Sprite(
                graphics.img.gui_radio,
                batch=gui.batch,
                group=graphics.group.gui_mid)
            sprite.opacity = 127
            sprite.scale = 0.75
            label = pyglet.text.Label(
                text,
                font_size=11, bold=False,
                color=(255, 255, 255, 127),
                batch=gui.batch,
                group=graphics.group.gui_front)
            self.sprites.append(sprite)
            self.labels.append(label)

        gui.app.window.push_handlers(self.on_resize, self.on_key_press, self.on_mouse_press)

    def _update_positions(self, height):
        sprite_x = self.padding + graphics.img.gui_radio.width//2
        label_x = sprite_x + graphics.img.gui_radio.width
        row_y = height/2 + (graphics.img.gui_radio.height + self.padding) * len(self.sprites)/2 + self.padding
        for i, (sprite, label) in enumerate(zip(self.sprites, self.labels)):
            row_y -= sprite.height + self.padding
            sprite.x = sprite_x
            label.x = label_x
            sprite.y = row_y
            label.y = row_y - (sprite.height - label.content_height)//2
            if i == self.index:
                self.check_sprite.x = sprite_x
                self.check_sprite.y = row_y

    @property
    def index(self):
        return self._index

    def set_index(self, value):
        self._index = value
        self.gui.app.change_mode(self.mode_data[value][1])
        self.check_sprite.x = self.sprites[value].x
        self.check_sprite.y = self.sprites[value].y

    def on_resize(self, width, height):
        self._update_positions(height)

    def on_key_press(self, symbol, modifiers):
        if not modifiers & (key.MOD_ALT | key.MOD_CTRL | key.MOD_SHIFT):
            symbols, mode_classes = zip(*self.mode_data)
            if symbol in symbols:
                self.set_index(symbols.index(symbol))

    def on_mouse_press(self, x, y, buttons, modifiers):
        for i, sprite in enumerate(self.sprites):
            is_hit = geometry.point_in_rect(
                    (x, y),
                    sprite.x-sprite.width/2, sprite.y-sprite.height/2,
                    sprite.width, sprite.height)
            if is_hit:
                self.set_index(i)
                return pyglet.event.EVENT_HANDLED
