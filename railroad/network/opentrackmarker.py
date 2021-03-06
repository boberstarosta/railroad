
import pyglet

from .statictrackobject import StaticTrackObject
from .. import graphics


class OpenTrackMarker(StaticTrackObject):
    
    def __init__(self, network, parent_segment, t, rotated=False):
        super().__init__(network, parent_segment, t, rotated)
        self.sprite = pyglet.sprite.Sprite(graphics.img.arrow_blue, batch=network.app.batch, group=graphics.group.signal)
        self.sprite.scale = 200 / self.sprite.image.height
        self.update_sprite_pos()
    
    def delete(self):
        super().delete()
        self.sprite.delete()
    
    def update_sprite_pos(self):
        direction = (self.parent_segment.nodes[1].position - self.parent_segment.nodes[0].position).normalized
        if self.rotated:
            direction = -direction
        self.sprite.position = self.position
        self.sprite.rotation = -direction.angle
    
    def on_t_changed(self, t):
        self.update_sprite_pos()
    
    def on_rotated_changed(self, rotated):
        self.update_sprite_pos()

