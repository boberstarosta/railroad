
import pyglet
from .basemode import BaseMode
from .. import geometry


class AddTrackObjectMode(BaseMode):

    name = "Add track object"
    def __init__(self, app):
        super().__init__(app)
        self.track_object_class = app.gui.track_object_select.selected_class
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            mouse = self.app.camera.to_world(x, y)
            nearest_segment = self.app.network.get_nearest_track_segment(mouse, max_distance=self.search_radius)
            if nearest_segment is not None:
                t = geometry.nearest_t_on_line(mouse, nearest_segment.nodes[0].position, nearest_segment.nodes[1].position)
                self.track_object_class(self.app.network, nearest_segment, t)
