
import pyglet
from .basemode import BaseMode
from .. import graphics
from .. import geometry
from ..network.scanners import Scanner


class DebugMode(BaseMode):
    name = "Debug"

    def __init__(self, app):
        super().__init__(app)
        self.label = pyglet.text.Label(
            "", font_name="mono", font_size=10, color=(255, 255, 255, 255),
            x=self.app.window.width/2 - 200, y=self.app.window.height-20,
            width=400, multiline=True, group=graphics.group.gui_front,
            batch=self.app.gui.batch
        )

        self.arrow_sprite_forward = pyglet.sprite.Sprite(
            graphics.img.arrow_violet,
            batch=self.app.batch,
            group=graphics.group.gui_front,
        )
        self.arrow_sprite_forward.scale = 400 / self.arrow_sprite_forward.height
        self.arrow_sprite_forward.visible = False

        self.arrow_sprite_backward = pyglet.sprite.Sprite(
            graphics.img.arrow_violet,
            batch=self.app.batch,
            group=graphics.group.gui_front,
        )
        self.arrow_sprite_backward.scale = 400 / self.arrow_sprite_backward.height
        self.arrow_sprite_backward.visible = False

        self.mouse = self.app.camera.to_world(0, 0)
        self.nearest_segment = None
        self.nearest_t = None

    def on_delete(self):
        self.label.delete()
        self.arrow_sprite_forward.delete()
        self.arrow_sprite_backward.delete()

    def update_scanner(self, sprite, backwards, length=1000):
        if self.nearest_segment is not None:
            scanner = Scanner(self.nearest_segment, self.nearest_t, backwards, length)
            if scanner.final_segment is not None:
                sprite.position = scanner.final_segment.position_from_t(scanner.final_t)
                if scanner.final_backwards:
                    sprite.rotation = -(-scanner.final_segment.direction).angle
                else:
                    sprite.rotation = -(scanner.final_segment.direction).angle
                sprite.visible = True
                return
        sprite.visible = False

    def update(self, x, y):
        self.mouse = self.app.camera.to_world(x, y)
        self.nearest_segment = self.app.network.get_nearest_track_segment(self.mouse, self.search_radius)
        if self.nearest_segment is not None:
            self.nearest_t = geometry.nearest_t_on_line(
                self.mouse, self.nearest_segment.nodes[0].position, self.nearest_segment.nodes[1].position)
        else:
            self.nearest_t = None

        self.update_scanner(self.arrow_sprite_forward, False)
        self.update_scanner(self.arrow_sprite_backward, True)

        self.label.text = "\n".join([
            "len(traincars): {}".format(len(self.app.trains.traincars)),
            "segment: {}".format(self.nearest_segment),
            "t: {}".format(self.nearest_t),
        ])

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            self.update(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            self.update(x, y)
