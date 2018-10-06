
from .basesceneryobject import BaseSceneryObject
from railroad import graphics


class Tree(BaseSceneryObject):

    image = graphics.img.tree

    def __init__(self, network, position, rotation=0):
        super().__init__(network, self.image, position, rotation)
