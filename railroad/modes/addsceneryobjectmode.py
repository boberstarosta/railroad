
import pyglet
import random
from ..network.sceneryobject import SceneryObject
from .basemode import BaseMode


class AddSceneryObjectMode(BaseMode):

    name = "Add scenery object"

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            SceneryObject(self.app.network, mouse, random.uniform(0, 359.99))
