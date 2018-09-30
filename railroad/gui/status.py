
import pyglet
from .. import graphics


class Status:
    def __init__(self, gui):
        self.gui = gui
        self.label = pyglet.text.Label(
            "", font_size=11, bold=False, color=(255, 255, 255, 127),
            x=10, y=self.gui.app.window.height - 10,
            width=gui.app.window.width//4,
            anchor_x="left", anchor_y="top", align="left", multiline=True,
            batch=gui.batch, group=graphics.group.gui_front
        )
        gui.app.window.push_handlers(self.on_resize)

    def on_resize(self, width, height):
        self.label.y = height - 10

    def generate_text(self):
        camera_pos = "{:.1f}, {:.1f}".format(self.gui.app.camera.position.x/100, self.gui.app.camera.position.y/100)
        zoom = "{:.0f} m".format(15 / self.gui.app.camera.zoom)
        fps = "{:.2f}".format(pyglet.clock.get_fps())

        return "Camera position: {}\nCamera height: {}\nFPS: {}"\
            .format(camera_pos, zoom, fps)

    def update(self, dt):
        self.label.text = self.generate_text()
