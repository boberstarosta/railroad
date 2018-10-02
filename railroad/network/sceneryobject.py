
import pyglet
from .. import graphics
from ..vec import Vec


class SceneryObject:

    def __init__(self, network, position, rotation=0):
        self.network = network
        self.sprite = pyglet.sprite.Sprite(
            graphics.img.tree,
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

    @property
    def position(self):
        return Vec(self.sprite.position)

    @position.setter
    def position(self, value):
        if value != self.sprite.position:
            self.sprite.position = value

    @property
    def rotation(self):
        return self.sprite.rotation

    @rotation.setter
    def rotation(self, value):
        if value != self.sprite.rotation:
            self.sprite.rotation = value
