
import pyglet
from .. import graphics


class BaseModel:

    image = None
    length = 0.0
    width = 0.0
    wheelbase = 0.0
    mass = 0.0
    has_engine = False

    @classmethod
    def create_sprite(cls, batch):
        sprite = pyglet.sprite.Sprite(
            cls.image,
            batch=batch,
            group=graphics.group.trains
        )
        sprite.scale_x = cls.length / cls.image.width
        sprite.scale_y = cls.width / cls.image.height
        return sprite


class LocoHeavy(BaseModel):

    image = graphics.img.loco_heavy
    length = 1755.0
    width  = 295.0
    wheelbase = 1280.0
    mass = 116500.0
    has_engine = True


class TrainCarBulk(BaseModel):

    image = graphics.img.traincar_bulk
    length = 1400.0
    width  = 300.0
    wheelbase = 850.0
    mass = 20500.0
    has_engine = False
