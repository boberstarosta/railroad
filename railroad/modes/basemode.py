class BaseMode:
    min_track_length = 500  # 5 meters
    _search_radius = 40  # 40 screen pixels

    def __init__(self, app):
        self.app = app

    def delete(self):
        self.on_delete()
    
    @property
    def search_radius(self):
        return self._search_radius / self.app.camera.zoom

    def on_key_press(self, symbol, modifiers): pass

    def on_mouse_motion(self, x, y, dx, dy): pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers): pass

    def on_mouse_press(self, x, y, buttons, modifiers): pass

    def on_mouse_release(self, x, y, buttons, modifiers): pass

    def on_delete(self): pass

