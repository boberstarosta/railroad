
import pyglet
from pyglet.window import key
from .. import graphics
from .. import geometry


class RadioGroup:

    sprite_scale = 0.6

    def __init__(self, gui, data, align_x, align_y, padding):
        self.gui = gui
        self.data = data
        self.align_x = align_x
        self.align_y = align_y
        self.padding = padding
        self._index = 0

        self.check_sprite = pyglet.sprite.Sprite(
            graphics.img.gui_radio_check, batch=gui.batch, group=graphics.group.gui_front)
        self.check_sprite.scale = self.sprite_scale

        self.sprites = []
        self.labels = []

        for symbol, caption in self.data:
            text = "[{}] ".format(key.symbol_string(symbol))
            text += caption
            sprite = pyglet.sprite.Sprite(
                graphics.img.gui_radio,
                batch=gui.batch,
                group=graphics.group.gui_mid)
            sprite.opacity = 127
            sprite.scale = self.sprite_scale
            label = pyglet.text.Label(
                text,
                font_size=11, bold=False,
                anchor_y="center",
                color=(255, 255, 255, 127),
                batch=gui.batch,
                group=graphics.group.gui_front)
            self.sprites.append(sprite)
            self.labels.append(label)

        gui.app.window.push_handlers(self.on_resize, self.on_key_press, self.on_mouse_press)
    
    @property
    def width(self):
        return graphics.img.gui_radio.width + 2*self.padding + max([l.content_width for l in self.labels])
    
    @property
    def height(self):
        return graphics.img.gui_radio.height * (len(self.sprites) - 0.5)
    
    def _calculate_sprite_x(self, width):
        align_dict = {
            "left": 0,
            "center": width/2 - self.width/2,
            "right": width - self.width
        }
        return align_dict[self.align_x] + graphics.img.gui_radio.width/2

    def _calculate_row_y(self, height):
        align_dict = {
            "bottom": self.height,
            "center": height/2 + self.height/2,
            "top": height,
        }
        return align_dict[self.align_y]
    
    def _update_positions(self, width, height):
        sprite_x = self._calculate_sprite_x(width)
        label_x = sprite_x + graphics.img.gui_radio.width/2
        row_y = self._calculate_row_y(height)
        print(height, self.height, row_y)
        for i, (sprite, label) in enumerate(zip(self.sprites, self.labels)):
            sprite.x = sprite_x
            label.x = label_x
            sprite.y = row_y
            label.y = row_y
            if i == self.index:
                self.check_sprite.x = sprite_x
                self.check_sprite.y = row_y
            row_y -= sprite.height + self.padding

    def _set_index(self, value):
        self._index = value
        self.check_sprite.x = self.sprites[value].x
        self.check_sprite.y = self.sprites[value].y
        self.on_index_changed(value)

    def on_resize(self, width, height):
        self._update_positions(width, height)

    def on_key_press(self, symbol, modifiers):
        if not modifiers & (key.MOD_ALT | key.MOD_CTRL | key.MOD_SHIFT):
            symbols, captions = zip(*self.data)
            if symbol in symbols:
                self._set_index(symbols.index(symbol))

    def on_mouse_press(self, x, y, buttons, modifiers):
        for i, sprite in enumerate(self.sprites):
            is_hit = geometry.point_in_rect(
                    (x, y),
                    sprite.x-sprite.width/2, sprite.y-sprite.height/2,
                    sprite.width, sprite.height)
            if is_hit:
                self._set_index(i)
                return pyglet.event.EVENT_HANDLED
    
    @property
    def index(self):
        return self._index

