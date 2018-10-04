
import pyglet
from railroad.network.statictrackobject import StaticTrackObject
from railroad import graphics
from railroad.vec import Vec


class BaseSignal(StaticTrackObject):
    
    height = 300
    corona_height = 70
    corona_start = 32
    corona_spacing = 49.5
    blink_interval = 0.3
    offset = 200
    
    image = None
    corona_images = []
    
    def __init__(self, network, parent_segment, t, rotated):
        super().__init__(network, parent_segment, t, rotated)
        self.sprite = pyglet.sprite.Sprite(self.image, batch=network.app.batch, group=graphics.group.signal)
        self.sprite.scale = self.height / self.sprite.image.height
        self.corona_sprites = [
            pyglet.sprite.Sprite(ci, batch=network.app.batch, group=graphics.group.corona) for ci in self.corona_images ]
        for cs in self.corona_sprites:
            cs.scale = self.corona_height / cs.image.height
            cs.visible = False
        self.blink_timer = 0.0
        self.blink_state = True
        self.light_states = []
        self.update_sprite_pos()
    
    def delete(self):
        super().delete()
        self.sprite.delete()
        for corona_sprite in self.corona_sprites:
            corona_sprite.delete()
    
    def update(self, dt):
        self.blink_timer -= dt
        if self.blink_timer <= 0:
            self.blink_timer = self.blink_interval
            self.blink_state = not self.blink_state
        self.update_setting()
        self.update_lights()
    
    def update_sprite_pos(self):
        direction = (self.parent_segment.nodes[1].position - self.parent_segment.nodes[0].position).normalized
        if self.rotated:
            direction = -direction
        perp = Vec(direction.y, -direction.x)
        position = self.position + direction*self.sprite.height/2 + perp*self.offset
        self.sprite.position = position
        self.sprite.rotation = -direction.angle
        for i, corona in enumerate(self.corona_sprites):
            corona.position = position + direction*self.height/2 - direction*self.corona_start - direction*i*self.corona_spacing
    
    def on_t_changed(self, t):
        self.update_sprite_pos()
    
    def on_rotated_changed(self, rotated):
        self.update_sprite_pos()
    
    def update_lights(self):
        for i, state in enumerate(self.light_states):
            if state == 0:
                self.corona_sprites[i].visible = False
            if state == 1:
                self.corona_sprites[i].visible = True
            if state == 2:
                self.corona_sprites[i].visible = self.blink_state

    def update_setting(self):
        pass

