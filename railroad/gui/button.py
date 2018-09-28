
import pyglet
from .. import geometry
from .. import graphics


class Button:

    image_back = graphics.img.button_background
    image_pressed = graphics.img.button_pressed

    def __init__(self, gui, image, x=0, y=0, action=None):
        self.gui = gui

        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=gui.batch, group=graphics.group.gui_front)
        self.sprite_back = pyglet.sprite.Sprite(self.image_back, x=x, y=y, batch=gui.batch,
                                                group=graphics.group.gui_back)
        self.sprite_pressed = pyglet.sprite.Sprite(self.image_pressed, x=x, y=y, batch=gui.batch,
                                                   group=graphics.group.gui_back)
        self.sprite_pressed.visible = False

        self.rect = (
            x - self.sprite.width // 2,
            y - self.sprite.height // 2,
            self.sprite.width,
            self.sprite.height)
        self.action = action
        self._pressed = False

        gui.app.window.push_handlers(self.on_mouse_press)
        gui.app.window.push_handlers(self.on_mouse_release)

    def delete(self):
        self.gui.app.window.remove_handler("on_mouse_press", self.on_mouse_press)
        self.gui.app.window.remove_handler("on_mouse_release", self.on_mouse_release)
        self.sprite.delete()
        self.sprite_back.delete()
        self.sprite_pressed.delete()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT and geometry.point_in_rect((x, y), *self.rect):
            self._pressed = True
            self.sprite_back.visible = False
            self.sprite_pressed.visible = True
            return pyglet.event.EVENT_HANDLED

    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            self.sprite_back.visible = True
            self.sprite_pressed.visible = False
            if geometry.point_in_rect((x, y), *self.rect):
                if callable(self.action):
                    self.action()
                return pyglet.event.EVENT_HANDLED


class ChangeModeButton(Button):

    def __init__(self, gui, image, mode_class, x=0, y=0):
        super().__init__(gui, image, x, y, self.do_action)
        self.mode_class = mode_class

    def do_action(self):
        self.gui.app.change_mode(self.mode_class)
