
import pyglet
from railroad import graphics
from railroad.vec import Vec


class BaseSceneryObject:

    image = None

    def __init__(self, network, position, rotation=0):
        self.network = network
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x=position[0], y=position[1],
            batch=network.app.batch,
            group=graphics.group.top
        )
        self.sprite.scale = 1000 / self.sprite.image.height  # 400 cm
        self.sprite.rotation = rotation
        network.scenery_objects.append(self)

    def delete(self):
        self.sprite.delete()
        self.network.scenery_objects.remove(self)

    def on_position_changed(self, position):
        pass

    def on_rotation_changed(self, rotation):
        pass

    @property
    def position(self):
        return Vec(self.sprite.position)

    @position.setter
    def position(self, value):
        if value != self.sprite.position:
            self.sprite.position = value
            self.on_position_changed(value)

    @property
    def rotation(self):
        return self.sprite.rotation

    @rotation.setter
    def rotation(self, value):
        if value != self.sprite.rotation:
            self.sprite.rotation = value
            self.on_rotation_changed(value)
