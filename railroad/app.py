
import pyglet
from pyglet.gl import *
from .camera import Camera
from .gui.gui import Gui
from .modes import *
from .network.network import Network


class App:
    
    def __init__(self, width=1500, height=800):
        self.window = pyglet.window.Window(caption = "railroad", width=width, height=height, resizable=True)
        self.window.set_minimum_size(800, 600)
        self.window.push_handlers(self)
        self.batch = pyglet.graphics.Batch()
        self.camera = Camera(self.window)
        self.network = Network(self)
        self.gui = Gui(self)
        self.fps_display = pyglet.window.FPSDisplay(self.window)
        self.mode = None
        pyglet.clock.schedule_interval(self.camera.update, 1/60)
        pyglet.clock.schedule_interval(self.network.update, 1/20)
        pyglet.clock.schedule_interval(self.gui.update, 1/60)

    def change_mode(self, mode_class):
        if type(self.mode) is not mode_class:
            if self.mode is not None:
                self.mode.delete()
            self.mode = mode_class(self)
            text = "Mode: " + (type(self.mode).__name__ if self.mode.name is None else self.mode.name)
            self.gui.show_notification(text)

    def on_key_press(self, symbol, modifiers):
        self.mode.on_key_press(symbol, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mode.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mode.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.RIGHT:
            self.camera.move_to_window_coords(x, y)
        self.mode.on_mouse_press(x, y, buttons, modifiers)

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.mode.on_mouse_release(x, y, buttons, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.camera.zoom_in()
        elif scroll_y < 0:
            self.camera.zoom_out()

    def on_draw(self):
        glClearColor(0.10, 0.30, 0.05, 1.0)
        self.window.clear()
        self.camera.apply_world_projection()
        self.batch.draw()
        self.camera.apply_gui_projection()
        self.gui.draw()
        self.fps_display.draw()
