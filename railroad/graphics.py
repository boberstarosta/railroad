from pyglet.gl import *


class EnableBlendGroup(pyglet.graphics.Group):

    def set_state(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


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

    loco_heavy    = pyglet.resource.image("data/trains/loco heavy.png")
    traincar_bulk = pyglet.resource.image("data/trains/traincar bulk.png")
    traincar_test = pyglet.resource.image("data/trains/traincar test.png")

    tree          = pyglet.resource.image("data/tree.png")

    gui_frame_top    = pyglet.resource.image("data/gui/frame top.png")
    gui_frame_middle = pyglet.resource.image("data/gui/frame mid.png")
    gui_radio        = pyglet.resource.image("data/gui/radio.png")
    gui_radio_check  = pyglet.resource.image("data/gui/radio check.png")

    debug_arrow_violet  = pyglet.resource.image("data/debug/arrow violet.png")
    debug_traincar = pyglet.resource.image("data/debug/traincar.png")
    debug_wheel = pyglet.resource.image("data/debug/wheel.png")
    debug_length = pyglet.resource.image("data/debug/length.png")
    debug_distance = pyglet.resource.image("data/debug/distance.png")


for attr in [getattr(img, i) for i in dir(img)]:
    if isinstance(attr, pyglet.image.TextureRegion):
        attr.anchor_x = attr.width / 2
        attr.anchor_y = attr.height / 2


class tex:
    ground = pyglet.resource.texture("data/ground.jpg")
    ballast = pyglet.resource.texture("data/track ballast.png")
    rails = pyglet.resource.texture("data/track rails.png")


class group:
    ground  = pyglet.graphics.TextureGroup(tex.ground, parent=pyglet.graphics.OrderedGroup(0))

    ballast = pyglet.graphics.TextureGroup(tex.ballast, parent=EnableBlendGroup(parent=pyglet.graphics.OrderedGroup(1)))
    rails   = pyglet.graphics.TextureGroup(tex.rails, parent=EnableBlendGroup(parent=pyglet.graphics.OrderedGroup(2)))

    trains  = pyglet.graphics.OrderedGroup(10)
    signal  = pyglet.graphics.OrderedGroup(11)
    corona  = pyglet.graphics.OrderedGroup(12)

    top     = pyglet.graphics.OrderedGroup(20)

    node    = pyglet.graphics.OrderedGroup(30)
    arrow   = pyglet.graphics.OrderedGroup(31)

    gui_back  = pyglet.graphics.OrderedGroup(40)
    gui_mid = pyglet.graphics.OrderedGroup(41)
    gui_front = pyglet.graphics.OrderedGroup(42)
