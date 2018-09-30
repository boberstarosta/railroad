from pyglet.gl import *


class img:
    node          = pyglet.resource.image("data/node.png")
    arrow_green   = pyglet.resource.image("data/arrow green.png")
    arrow_red     = pyglet.resource.image("data/arrow red.png")
    arrow_blue    = pyglet.resource.image("data/arrow blue.png")
    signal        = pyglet.resource.image("data/signal.png")
    distant_signal= pyglet.resource.image("data/distant.png")
    block_signal  = pyglet.resource.image("data/block.png")
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
    ground = pyglet.resource.texture("data/ground.jpg")


class group:
    ground  = pyglet.graphics.TextureGroup(tex.ground, parent=pyglet.graphics.OrderedGroup(0))

    node    = pyglet.graphics.OrderedGroup(3)
    arrow   = pyglet.graphics.OrderedGroup(4)
    signal  = pyglet.graphics.OrderedGroup(5)
    corona  = pyglet.graphics.OrderedGroup(6)

    gui_back  = pyglet.graphics.OrderedGroup(12)
    gui_mid = pyglet.graphics.OrderedGroup(13)
    gui_front = pyglet.graphics.OrderedGroup(14)
