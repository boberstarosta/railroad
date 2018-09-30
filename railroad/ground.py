
from pyglet import gl
from . import graphics


class Ground:
    def __init__(self, app):
        self.app = app
        self.x = 0
        self.y = 0
        self.vertex_list = app.batch.add(4, gl.GL_QUADS, graphics.group.ground, "v2f", "t2i")
        self.update_vertices()
        app.camera.push_handlers(self.on_camera_changed)
        app.window.push_handlers(self.on_resize)

    def update_vertices(self):
        tile_width = graphics.tex.ground.width * 12
        tile_height = graphics.tex.ground.height * 12

        x = int(self.app.camera.position.x // tile_width)
        y = int(self.app.camera.position.y // tile_height)

        x_tiles = int((self.app.window.width / self.app.camera.zoom) // tile_width) + 2
        y_tiles = int((self.app.window.height / self.app.camera.zoom) // tile_height) + 2

        left_tile = x - x_tiles//2
        right_tile = left_tile + x_tiles + 1
        bottom_tile = y - y_tiles//2
        top_tile = bottom_tile + y_tiles + 1

        left = left_tile * tile_width
        right = right_tile * tile_width
        bottom = bottom_tile * tile_height
        top = top_tile * tile_height

        self.vertex_list.tex_coords = [
            left_tile, bottom_tile, left_tile, top_tile,
            right_tile, top_tile, right_tile, bottom_tile
        ]
        self.vertex_list.vertices = [left, bottom, left, top, right, top, right, bottom]

    def on_camera_changed(self, position, zoom):
        self.update_vertices()

    def on_resize(self, width, height):
        self.update_vertices()
