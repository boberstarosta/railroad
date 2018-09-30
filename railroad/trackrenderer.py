
from pyglet.gl import *
from .geometry import *
from . import graphics


class TrackRenderer:
    WIDTH = 250  # 2.5 m

    def __init__(self, edge):
        self.edge = edge
        self.vertex_list_ballast = None
        self.vertex_list_rails = None

    def delete(self):
        if self.vertex_list_ballast is not None:
            self.vertex_list_ballast.delete()
        if self.vertex_list_rails is not None:
            self.vertex_list_rails.delete()
        self.vertex_list_ballast = None
        self.vertex_list_rails = None

    def clear(self):
        self.delete()

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
            dir12 = Vec(0, 0) if length == 0 else (p2 - p1) / length
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

            vertices.extend([*r1] + [*l1] + [*l2] + [*r2])

            tw = length / self.WIDTH
            tex_coords.extend((
                0, 0,
                0, 1,
                tw, 1,
                tw, 0
            ))

        self.vertex_list_ballast = self.edge.network.app.batch.add(
            len(vertices)//2, pyglet.gl.GL_QUADS, graphics.group.ballast, "v2f", "t2f")
        self.vertex_list_rails = self.edge.network.app.batch.add(
            len(tex_coords)//2, pyglet.gl.GL_QUADS, graphics.group.rails, "v2f", "t2f")
        self.vertex_list_ballast.vertices = self.vertex_list_rails.vertices = vertices
        self.vertex_list_ballast.tex_coords = self.vertex_list_rails.tex_coords = tex_coords
