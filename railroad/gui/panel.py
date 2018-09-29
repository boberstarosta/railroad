import pyglet
from pyglet import gl
from .. import graphics
from .. import geometry


class Panel:
    width = 200
    padding = 10

    def __init__(self, gui):
        self.gui = gui
        self.sprite = None
        self.speed = 0
        self._hidden = False
        gui.app.window.push_handlers(self.on_resize, self.on_mouse_press)

    def _generate_image(self, height):
        width = graphics.img.gui_frame_top.width
        height -= 2 * self.padding

        texture = pyglet.image.Texture.create(width, height, rectangle=True)
        texture.anchor_x = 0
        texture.anchor_y = 0

        gl.glBindTexture(texture.target, texture.id)

        top = graphics.img.gui_frame_top.get_image_data()
        top.blit_to_texture(texture.target, 0, 0, height - graphics.img.gui_frame_top.height, gl.GL_RGBA)

        top_data = top.get_data("RGBA", 4 * top.width)
        bottom = pyglet.image.create(top.width, top.height)
        rows = [top_data[i:i + 4 * top.width] for i in range(0, len(top_data), 4 * top.width)]
        bottom_data = bytes([row[i] for row in reversed(rows) for i in range(len(row))])
        bottom.set_data("RGBA", 4 * bottom.width, bottom_data)
        bottom.image_data.blit_to_texture(texture.target, 0, 0, 0, gl.GL_RGBA)

        middle = graphics.img.gui_frame_middle.get_image_data()
        middle_height = height - graphics.img.gui_frame_top.height - graphics.img.gui_frame_top.height
        middle_data = middle.get_data("RGBA", 4 * middle.width)
        data = middle_data[:4 * middle.width] * middle_height
        middle_image = pyglet.image.create(middle.width, middle_height)
        middle_image.set_data('RGBA', middle.width * 4, data)
        y = graphics.img.gui_frame_top.height
        middle_image.image_data.blit_to_texture(texture.target, 0, 0, y, gl.GL_RGBA)

        return texture

    def on_resize(self, width, height):
        if self.sprite is not None:
            self.sprite.delete()
        image = self._generate_image(height)
        self.sprite = pyglet.sprite.Sprite(image, batch=self.gui.batch, group=graphics.group.gui_back)
        x = width if self._hidden else width - self.sprite.width - self.padding
        self.sprite.position = x, self.padding
        self.sprite.opacity = 127

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT \
        and geometry.point_in_rect((x, y), self.sprite.x, self.sprite.y, self.sprite.width, self.sprite.height):
            return pyglet.event.EVENT_HANDLED

    def hide(self):
        self.speed = 2000

    def show(self):
        self.speed = -2000

    def update(self, dt):
        if self.speed != 0:
            self.sprite.x += self.speed * dt
            if self.sprite.x < self.gui.app.window.width - self.sprite.width - self.padding:
                self._hidden = False
                self.speed = 0
                self.sprite.x = self.gui.app.window.width - self.sprite.width - self.padding
            elif self.sprite.x > self.gui.app.window.width:
                self._hidden = True
                self.speed = 0
                self.sprite.x = self.gui.app.window.width

    @property
    def hidden(self):
        return self._hidden
