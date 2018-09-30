
from pyglet.gl import *
from .geometry import *


class TrackRenderer:

    WIDTH = 200  # 2 m
    instances = []
    texture_ballast = pyglet.resource.texture("data/track ballast.png")
    texture_rails = pyglet.resource.texture("data/track rails.png")

    @classmethod
    def draw(cls):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(cls.texture_ballast.target, cls.texture_ballast.id)
        glBegin(GL_QUADS)
        for instance in cls.instances:
            for vertex, tex_coord in zip(instance.vertices, instance.tex_coords):
                glTexCoord2fv(tex_coord)
                glVertex2fv(vertex)
        glEnd()
        glBindTexture(cls.texture_rails.target, cls.texture_rails.id)
        glBegin(GL_QUADS)
        for instance in cls.instances:
            for vertex, tex_coord in zip(instance.vertices, instance.tex_coords):
                glTexCoord2fv(tex_coord)
                glVertex2fv(vertex)
        glEnd()

    def __init__(self, edge):
        self.edge = edge
        self.vertices = []
        self.tex_coords = []
        self.instances.append(self)

    def delete(self):
        self.instances.remove(self)

    def clear(self):
        self.vertices = []
        self.tex_coords = []

    def update_track(self):
        vertices = []
        tex_coords = []

        half_width = self.WIDTH / 2

        for segment in self.edge.track_segments:
            prev_segment = segment.nodes[0].other_segment(segment)
            next_segment = segment.nodes[1].other_segment(segment)

            p0 = None if prev_segment is None else prev_segment.other_node(segment.nodes[0]).position
            p1 = segment.nodes[0].position
            p2 = segment.nodes[1].position
            p3 = None if next_segment is None else next_segment.other_node(segment.nodes[1]).position

            length = (p2 - p1).length
            dir12 = (p2 - p1) / length
            dir12perp = Vec(-dir12.y, dir12.x)

            l_start = p1 + dir12perp * half_width
            r_start = p1 - dir12perp * half_width
            l_end = p2 + dir12perp * half_width
            r_end = p2 - dir12perp * half_width

            if p0 is None:
                l1 = l_start
                r1 = r_start
            else:
                p0p2dir = (p2 - p0).normalized
                side1dir = Vec(-p0p2dir.y, p0p2dir.x)
                intersect = intersect_point(l_start, dir12, p1, side1dir)
                l1 = l_start if intersect is None else intersect
                intersect = intersect_point(r_start, dir12, p1, side1dir)
                r1 = r_start if intersect is None else intersect

            if p3 is None:
                l2 = l_end
                r2 = r_end
            else:
                p1p3dir = (p3 - p1).normalized
                side2dir = Vec(-p1p3dir.y, p1p3dir.x)
                intersect = intersect_point(l_start, dir12, p2, side2dir)
                l2 = l_end if intersect is None else intersect
                intersect = intersect_point(r_start, dir12, p2, side2dir)
                r2 = r_end if intersect is None else intersect

            vertices.extend(((GLfloat*2)(*r1), (GLfloat*2)(*l1), (GLfloat*2)(*l2), (GLfloat*2)(*r2)))

            tx = length / self.WIDTH
            tex_coords.extend((
                (GLfloat*2)(0, 0),
                (GLfloat*2)(0, 1),
                (GLfloat*2)(tx, 1),
                (GLfloat*2)(tx, 0)
            ))

        self.vertices = vertices
        self.tex_coords = tex_coords
