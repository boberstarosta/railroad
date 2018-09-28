
import pyglet

from .baseedge import BaseEdge
from .. import graphics
from ..geometry import intersect_point
from ..vec import Vec


class TrackSegment(BaseEdge):
    
    def __init__(self, network, parent_edge, node1, node2):
        super().__init__(node1, node2)
        self.network = network
        self.parent_edge = parent_edge
        self.vertex_list_ballast = network.app.batch.add(4, pyglet.gl.GL_QUADS, graphics.group.ballast, "v2f", "t2f")
        self.vertex_list_rails = network.app.batch.add(4, pyglet.gl.GL_QUADS, graphics.group.rails, "v2f", "t2f")
        # Edge is now calling update_vertex_list() for all its children
        #self.update_vertex_list()
        self.track_objects = []
        self.network.track_segments.append(self)
    
    def delete(self):
        super().delete()
        self.vertex_list_ballast.delete()
        self.vertex_list_rails.delete()
        self.network.track_segments.remove(self)
        while len(self.track_objects) > 0:
            self.track_objects[-1].delete()
    
    @staticmethod
    def _is_valid_signal(to, to_class, rotated, min_t, max_t, exclude):
        return (
            isinstance(to, to_class)
            and to.rotated == rotated
            and (min_t is None or to.t >= min_t)
            and (max_t is None or to.t <= max_t)
            and to not in exclude
        )
    
    def nearest_track_object(self, to_class, node, min_t=None, max_t=None, exclude=None):
        if exclude is None:
            exclude = []
        if node is self.nodes[0]:
            rotated = False
        elif node is self.nodes[1]:
            rotated = True
        else:
            raise ValueError("TrackSegment.nearest_signal:  Not my node.")
        valid_objects = [to for to in self.track_objects if self._is_valid_signal(to, to_class, rotated, min_t, max_t, exclude)]
        if len(valid_objects) > 0:
            valid_objects.sort(key=lambda to: to.t, reverse=rotated)
            return valid_objects[0]
        else:
            return None
    
    def update_vertex_list(self):
        prev_edge = self.nodes[0].other_segment(self)
        next_edge = self.nodes[1].other_segment(self)
        
        width = 200  # 2 m
        
        p0 = None if prev_edge is None else prev_edge.other_node(self.nodes[0]).position
        p1 = self.nodes[0].position
        p2 = self.nodes[1].position
        p3 = None if next_edge is None else next_edge.other_node(self.nodes[1]).position
        
        dir12 = (p2 - p1).normalized
        dir12perp = Vec(-dir12.y, dir12.x)
        
        l_start = p1 + dir12perp * width/2
        r_start = p1 - dir12perp * width/2
        l_end = p2 + dir12perp * width/2
        r_end = p2 - dir12perp * width/2
        
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
            
        self.vertex_list_ballast.vertices = [
            r1.x, r1.y, l1.x, l1.y, l2.x, l2.y, r2.x, r2.y
        ]

        length = (p2 - p1).length
        tx = length / width
        
        tl1x = 0 * tx
        tl1y = 1
        tr1x = 0 * tx
        tr1y = 0
        tl2x = 1 * tx
        tl2y = 1
        tr2x = 1 * tx
        tr2y = 0
        self.vertex_list_ballast.tex_coords = [
            tr1x, tr1y, tl1x, tl1y, tl2x, tl2y, tr2x, tr2y
        ]
        
        self.vertex_list_rails.vertices = self.vertex_list_ballast.vertices
        self.vertex_list_rails.tex_coords = self.vertex_list_ballast.tex_coords



