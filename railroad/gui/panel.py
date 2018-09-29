
import pyglet
from pyglet import gl
from .. import graphics
from .. import geometry


class Panel:

    width = 200

    def __init__(self, gui):
        self.gui = gui
        self.sprite = None
        gui.app.window.push_handlers(self.on_resize, self.on_mouse_press)

    def _generate_vertices(self, width, height):
        return (
            width - 1 - self.width, 0,
            width - 1 - self.width, height - 1,
            width - 1, height - 1,
            width, 0
        )

    def _generate_image(self, height):
        width = graphics.img.gui_frame_top.width

        texture = pyglet.image.Texture.create(width, height, rectangle=True)
        texture.anchor_x = 0
        texture.anchor_y = 0

        gl.glBindTexture(texture.target, texture.id)
        graphics.img.gui_frame_top.image_data.blit_to_texture(
            texture.target, 0, 0, height-graphics.img.gui_frame_top.height, gl.GL_RGBA)
        graphics.img.gui_frame_bottom.image_data.blit_to_texture(
            texture.target, 0, 0, 0, gl.GL_RGBA)

        # Trying to access middle image data
        middle_data = graphics.img.gui_frame_middle.get_image_data()
        data_width = middle_data.width
        data = middle_data.get_data("RGBA", 4 * data_width)

        # pos = (data_width * y + x) * 4
        # rgba = map(ord, data[pos:pos + 3])

        # TODO: Create a new image of the right size and fill it with data
        # middle_height = height - graphics.img.gui_frame_top.height - graphics.img.gui_frame_bottom.height
        # new_image.set_data('RGBA', middle_data.width * 4, data)

        y = graphics.img.gui_frame_bottom.height
        graphics.img.gui_frame_middle.image_data.blit_to_texture(
            texture.target, 0, 0, y, gl.GL_RGBA)

        return texture

    def on_resize(self, width, height):
        if self.sprite is not None:
            self.sprite.delete()
        image = self._generate_image( height)
        self.sprite = pyglet.sprite.Sprite(image, batch=self.gui.batch, group=graphics.group.gui_back)
        self.sprite.position = width - self.sprite.width, 0
        self.sprite.opacity = 95
        self.rect = (self.sprite.x, self.sprite.y, self.sprite.width, self.sprite.height)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT and geometry.point_in_rect((x, y), *self.rect):
            return pyglet.event.EVENT_HANDLED

    def update(self, dt):
        pass
