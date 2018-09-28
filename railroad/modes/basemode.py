
import pyglet


class BaseMode:
    min_track_length = 500  # 5 meters
    _search_radius = 40  # 40 screen pixels

    def __init__(self, app):
        self.app = app
        self.app.window.push_handlers(self)
    
    def delete(self):
        self.app.window.pop_handlers()
    
    def update(self, dt):
        pass
    
    @property
    def search_radius(self):
        return self._search_radius / self.app.camera.zoom

