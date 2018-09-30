from pyglet.gl import *

from .vec import Vec


class Camera(pyglet.event.EventDispatcher):
    
    def __init__(self, window, position=Vec(0,0), zoom_index=7,
                 zoom_levels=None, zoom_move_time=0.5):
        if zoom_levels is None:
            factor = 2
            zoom_levels = [1/i**factor for i in range(10, 0, -1)]
        self.window = window

        self._position = position
        self.position_from = self.position
        self.position_to = self.position
        self.timer = 0.0
        self.tween_time = 0.0
        
        self.zoom_index = zoom_index
        self.zoom_from = self.zoom_index
        self.zoom_to = self.zoom_index
        self.zoom_timer = 0.0
        self.zoom_tween_time = 0.0
        self.zoom_levels = zoom_levels
        self._zoom = self.zoom_levels[zoom_index]
        self.zoom_move_time = zoom_move_time

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value != self._position:
            self._position = value
            self.dispatch_event("on_camera_changed", self.position, self.zoom)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        if value != self._zoom:
            self._zoom = value
            self.dispatch_event("on_camera_changed", self.position, self.zoom)

    def update(self, dt):
        if self.timer < self.tween_time:
            self.timer += dt
            t = self.timer / self.tween_time
            tween_value = 1 - (t-1)**4
            move = (self.position_to - self.position_from) * tween_value
            self.position = self.position_from + move
        else:
            self.position = self.position_to
        
        if self.zoom_timer < self.zoom_tween_time:
            self.zoom_timer += dt
            t = self.zoom_timer / self.zoom_tween_time
            tween_value = 1 - (t-1)**4
            move = (self.zoom_to - self.zoom_from) * tween_value
            self.zoom = self.zoom_from + move
        else:
            self.zoom = self.zoom_levels[self.zoom_index]
    
    def move_to_window_coords(self, x, y, time=1):
        self.position_from = self.position
        self.position_to = Vec(self.to_world(x, y))
        self.timer = 0.0
        self.tween_time = time
    
    def zoom_in(self):
        if self.zoom_index < len(self.zoom_levels) - 1:
            self.zoom_index += 1
            self.zoom_from = self.zoom
            self.zoom_to = self.zoom_levels[self.zoom_index]
            self.zoom_timer = 0.0
            self.zoom_tween_time = self.zoom_move_time
    
    def zoom_out(self):
        if self.zoom_index > 0:
            self.zoom_index -= 1
            self.zoom_from = self.zoom
            self.zoom_to = self.zoom_levels[self.zoom_index]
            self.zoom_timer = 0.0
            self.zoom_tween_time = self.zoom_move_time
    
    def to_world(self, x, y):
        win_pos = Vec(x - self.window.width//2, y - self.window.height//2) / self.zoom
        return win_pos + self.position
    
    def to_window(self, position):
        win_pos = (position - self.position) * self.zoom
        return int(win_pos.x), int(win_pos.y)
    
    def tile_rect(self, tile_size):
        world_x = self.position.x - self.window.width / self.zoom / 2
        world_y = self.position.y - self.window.height / self.zoom / 2
        tile_x = int(world_x // tile_size)
        tile_y = int(world_y // tile_size)
        world_w = self.window.width / self.zoom
        world_h = self.window.height / self.zoom
        tile_w = int(world_w // tile_size) + 1
        tile_h = int(world_h // tile_size) + 1
        return tile_x, tile_y, tile_x + tile_w, tile_y + tile_h
    
    def apply_world_projection(self):
        glViewport(0, 0, self.window.width, self.window.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-self.window.width/2, self.window.width/2, -self.window.height/2, self.window.height/2)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glScalef(self.zoom, self.zoom, 1)
        glTranslatef(-self.position.x, -self.position.y, 0)
    
    def apply_gui_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window.width, 0, self.window.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


Camera.register_event_type("on_camera_changed")
