
import pyglet
from .. import graphics


class BaseModel:

    image = None
    length = 0.0
    width = 0.0
    mass = 0.0
    has_engine = False

    @classmethod
    def create_sprite(cls):
        sprite = pyglet.sprite.Sprite(
            graphics.img.traincar_bulk,
            group=graphics.group.trains
        )
        sprite.scale_x = cls.width / cls.image.width
        return sprite


class LocoHeavy(BaseModel):

    image = graphics.img.traincar_bulk
    length = 1755.0
    width  = 295.0
    mass = 116500.0
    has_engine = True


class TrainCarBulk(BaseModel):

    image = graphics.img.traincar_bulk
    length = 1400.0
    width  = 300.0
    mass = 20500.0
    has_engine = False
