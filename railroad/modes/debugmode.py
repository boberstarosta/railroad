
import pyglet
from collections import namedtuple
from .basemode import BaseMode
from .. import graphics
from .. import geometry
from ..network.scanners import Scanner, DistanceScanner, TrackObjectScanner
from ..trains.traincar import TrainCar
from ..trains.wheel import Wheel
from ..trains.models import TrainCarBulk


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

        self.sprites_length = self.create_sprite_pair(graphics.img.debug_length)
        self.sprites_distance = self.create_sprite_pair(graphics.img.debug_distance)
        self.sprites_traincar = self.create_sprite_pair(graphics.img.debug_traincar)
        self.sprites_wheel= self.create_sprite_pair(graphics.img.debug_wheel)

        self.mouse = self.app.camera.to_world(0, 0)
        self.nearest_segment = None
        self.nearest_t = None

    def create_sprite_pair(self, image):
        sprite0 = pyglet.sprite.Sprite(
            image,
            batch=self.app.batch,
            group=graphics.group.gui_front
        )
        sprite0.scale = 400 / sprite0.height
        sprite0.visible = False

        sprite1 = pyglet.sprite.Sprite(
            image,
            batch=self.app.batch,
            group=graphics.group.gui_front
        )
        sprite1.scale = 400 / sprite1.height
        sprite1.visible = False

        return (sprite0, sprite1)

    def on_delete(self):
        self.label.delete()
        for i in range(2):
            self.sprites_length[i].delete()
            self.sprites_distance[i].delete()

    def update_length(self, sprite, backwards, length=3000):
        if self.nearest_segment is None:
            sprite.visible = False
            return
        scanner = Scanner(self.nearest_segment, self.nearest_t, backwards, length)
        if scanner.final_segment is not None:
            sprite.position = scanner.final_segment.position_from_t(scanner.final_t)
            if scanner.final_backwards:
                sprite.rotation = -(-scanner.final_segment.direction).angle
            else:
                sprite.rotation = -(scanner.final_segment.direction).angle
            sprite.visible = True

    def update_distance(self, sprite, backwards):
        if self.nearest_segment is None:
            sprite.visible = False
            return

        FakeTraincar = namedtuple("TrainCar", ("parent_segment", "t", "model"))
        fake_traincar = FakeTraincar(self.nearest_segment, self.nearest_t, TrainCarBulk)

        scanner = DistanceScanner(fake_traincar, backwards)
        sprite.position = scanner.final_segment.position_from_t(scanner.final_t)
        if scanner.final_reversed:
            sprite.rotation = -(-scanner.final_segment.direction).angle
        else:
            sprite.rotation = -(scanner.final_segment.direction).angle

        sprite.visible = True

    def update_traincar(self, sprite, backwards):
        if self.nearest_segment is None:
            sprite.visible = False
            return

        scanner = TrackObjectScanner(self.nearest_segment, self.nearest_t, backwards, TrainCar)

        if scanner.final_object is None:
            sprite.visible = False
            return

        sprite.position = scanner.final_segment.position_from_t(scanner.final_t)
        if scanner.final_object.rotated:
            sprite.rotation = -(-scanner.final_object.direction).angle
        else:
            sprite.rotation = -(scanner.final_object.direction).angle
        sprite.visible = True

    def update_wheel(self, sprite, backwards):
        if self.nearest_segment is None:
            sprite.visible = False
            return

        scanner = TrackObjectScanner(self.nearest_segment, self.nearest_t, backwards, Wheel)

        if scanner.final_object is None:
            sprite.visible = False
            return

        sprite.position = scanner.final_segment.position_from_t(scanner.final_t)
        if scanner.final_object.rotated:
            sprite.rotation = -(-scanner.final_object.parent_traincar.direction).angle
        else:
            sprite.rotation = -(scanner.final_object.parent_traincar.direction).angle
        sprite.visible = True

    def update(self, x, y):
        self.mouse = self.app.camera.to_world(x, y)
        self.nearest_segment = self.app.network.get_nearest_track_segment(self.mouse, self.search_radius)
        if self.nearest_segment is not None:
            self.nearest_t = geometry.nearest_t_on_line(
                self.mouse, self.nearest_segment.nodes[0].position, self.nearest_segment.nodes[1].position)
        else:
            self.nearest_t = None

        self.update_length(self.sprites_length[0], False)
        self.update_length(self.sprites_length[1], True)

        self.update_distance(self.sprites_distance[0], False)
        self.update_distance(self.sprites_distance[1], True)

        self.update_traincar(self.sprites_traincar[0], False)
        self.update_traincar(self.sprites_traincar[1], True)

        self.update_wheel(self.sprites_wheel[0], False)
        self.update_wheel(self.sprites_wheel[1], True)

        self.label.text = "\n".join([
            "len(traincars): {}".format(len(self.app.trains.traincars)),
            "len(consists): {}".format(len(self.app.trains.consists)),
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
