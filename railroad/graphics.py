from pyglet.gl import *


class TextureEnableGroup(pyglet.graphics.Group):
    
    def set_state(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)

    def unset_state(self):
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)


class TextureDisableGroup(pyglet.graphics.Group):

    def set_state(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_TEXTURE_2D)

    def unset_state(self):
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)


texture_enable_group = TextureEnableGroup()
texture_disable_group = TextureDisableGroup()

class OrderedTextureGroup(pyglet.graphics.OrderedGroup):

    def __init__(self, order, texture):
        super().__init__(order, parent=texture_enable_group)
        self.texture = texture

    def set_state(self):
        glBindTexture(self.texture.target, self.texture.id)

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.order == other.order and
                self.texture.id == other.texture.id and
                self.texture.target == other.texture.target and
                self.parent == other.parent)

    def __hash__(self):
        return hash((self.texture.id, self.texture.target))


class img:
    node          = pyglet.resource.image("data/node.png")
    arrow_green   = pyglet.resource.image("data/arrow green.png")
    arrow_red     = pyglet.resource.image("data/arrow red.png")
    arrow_blue    = pyglet.resource.image("data/arrow blue.png")
    signal        = pyglet.resource.image("data/signal.png")
    distant_signal= pyglet.resource.image("data/distant.png")
    corona_green  = pyglet.resource.image("data/corona green.png")
    corona_orange = pyglet.resource.image("data/corona orange.png")
    corona_red    = pyglet.resource.image("data/corona red.png")
    corona_white  = pyglet.resource.image("data/corona white.png")

    gui_frame_top    = pyglet.resource.image("data/gui/frame top.png")
    gui_frame_middle = pyglet.resource.image("data/gui/frame mid.png")
    gui_radio        = pyglet.resource.image("data/gui/radio.png")
    gui_radio_check  = pyglet.resource.image("data/gui/radio check.png")


for attr in [getattr(img, i) for i in dir(img)]:
    if isinstance(attr, pyglet.image.TextureRegion):
        attr.anchor_x = attr.width / 2
        attr.anchor_y = attr.height / 2


class tex:
    ballast = pyglet.resource.texture("data/track ballast.png")
    rails = pyglet.resource.texture("data/track rails.png")


class group:
    ballast = OrderedTextureGroup(1, tex.ballast)
    rails   = OrderedTextureGroup(2, tex.rails)
    node    = pyglet.graphics.OrderedGroup(3)
    arrow   = pyglet.graphics.OrderedGroup(4)
    signal  = pyglet.graphics.OrderedGroup(5)
    corona  = pyglet.graphics.OrderedGroup(6)

    gui_back  = pyglet.graphics.OrderedGroup(12, parent=texture_disable_group)
    gui_mid = pyglet.graphics.OrderedGroup(13, parent=texture_disable_group)
    gui_front = pyglet.graphics.OrderedGroup(14, parent=texture_disable_group)
