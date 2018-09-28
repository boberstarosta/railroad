
import pyglet
from pyglet.gl import *
from .camera import Camera
from railroad.network.network import Network
from .modes import *


class App:
    
    def __init__(self, width=1500, height=800):
        pyglet.clock.schedule_interval(self.on_fast_update, 1/60)
        pyglet.clock.schedule_interval(self.on_slow_update, 1/20)
        self.window = pyglet.window.Window(width=width, height=height, resizable=True)
        self.window.push_handlers(self)
        self.batch = pyglet.graphics.Batch()
        self.camera = Camera(self.window)
        self.network = Network(self)
        self.fps_display = pyglet.window.FPSDisplay(self.window)
        self.mode = None
    
    def change_mode(self, mode_class):
        if self.mode is not None:
            self.mode.delete()
        self.mode = mode_class(self)
    
    def on_key_press(self, symbol, modifiers):
        if not modifiers & pyglet.window.key.MOD_CTRL:
            if symbol == pyglet.window.key.A:
                self.change_mode(AddTrackMode)
            elif symbol == pyglet.window.key.M:
                self.change_mode(MoveTrackMode)
            elif symbol == pyglet.window.key.S:
                self.change_mode(StraightenTrackMode)
            elif symbol == pyglet.window.key.I:
                self.change_mode(InsertNodeMode)
            elif symbol == pyglet.window.key.J:
                self.change_mode(SwitchJunctionMode)
            elif symbol == pyglet.window.key.D:
                self.change_mode(DeleteTrackMode)
            elif symbol == pyglet.window.key.X:
                self.change_mode(RemoveNodeMode)
            elif symbol == pyglet.window.key.K:
                self.change_mode(AddTrackObjectMode)
            elif symbol == pyglet.window.key.R:
                self.change_mode(RotateTrackObjectMode)
            elif symbol == pyglet.window.key.O and modifiers & pyglet.window.key.MOD_SHIFT:
                self.network.show_nodes = not self.network.show_nodes
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.RIGHT:
            self.camera.move_to_window_coords(x, y)
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.camera.zoom_in()
        elif scroll_y < 0:
            self.camera.zoom_out()
    
    def on_fast_update(self, dt):
        self.camera.update(dt)

    def on_slow_update(self, dt):
        self.network.update(dt)

    def on_draw(self):
        glClearColor(0.10, 0.30, 0.05, 1.0)
        self.window.clear()
        self.camera.apply_world_projection()
        self.batch.draw()
        self.camera.apply_gui_projection()
        self.fps_display.draw()

