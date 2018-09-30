
import pyglet

from .basenode import BaseNode
from .tracknode import TrackNode
from .. import geometry
from .. import graphics


class Node(BaseNode):
    
    def __init__(self, network, position):
        super().__init__(position)
        self.network = network
        self.sprite = pyglet.sprite.Sprite(graphics.img.node, batch=network.app.batch, group=graphics.group.node)
        self.sprite.scale = 200 / self.sprite.image.height  # 200 cm
        self.sprite.position = position
        self.arrow_sprite = None
        self._is_switched = False
        self.network.nodes.append(self)
        self.track_node = TrackNode(self.network, self, self.position)
    
    def delete(self):
        super().delete()
        self.sprite.delete()
        self.network.nodes.remove(self)
        self.track_node.delete()
        if self.arrow_sprite is not None:
            self.arrow_sprite.delete()
    
    def add_edge(self, edge):
        super().add_edge(edge)
        self.update_arrow_sprite()

    def remove_edge(self, edge):
        super().remove_edge(edge)
        self.update_arrow_sprite()
    
    def other_edge(self, edge):
        if edge not in self.edges:
            raise ValueError("Node.other_edge: Not my edge")
        point = self.point
        if edge is point:
            return self.current_edge_set
        else:
            return point

    def switch(self):
        self._is_switched = not self._is_switched
        self.update_arrow_sprite()
    
    def update_arrow_sprite(self):
        if len(self.edges) == 3:
            if self.is_switched:
                arrow_image = graphics.img.arrow_red
            else:
                arrow_image = graphics.img.arrow_green
            self.arrow_sprite = pyglet.sprite.Sprite(arrow_image, batch=self.network.app.batch, group=graphics.group.arrow)
            self.arrow_sprite.scale = 300 / self.arrow_sprite.image.width  # 300 cm
            self.arrow_sprite.position = self.position
            current_edge_set_dir = (self.current_edge_set.other_node(self).position - self.position).normalized
            self.arrow_sprite.rotation = -current_edge_set_dir.angle
        else:
            if self.arrow_sprite is not None:
                self.arrow_sprite.delete()
                self.arrow_sprite = None
    
    def on_position_changed(self, position):
        self.sprite.position = position
        for edge in self._edges:
            edge.update_track()
            other_node = edge.other_node(self)
            for other_edge in other_node.other_edges(edge):
                other_edge.update_track()
        for edge in self._edges:
            edge.renderer.update_track()
            other_node = edge.other_node(self)
            for other_edge in other_node.other_edges(edge):
                other_edge.renderer.update_track()
        self.track_node.position = position
        self.update_arrow_sprite()
        for node in self.nodes:
            node.update_arrow_sprite()

    @property
    def is_switched(self):
        return self._is_switched
    
    @property
    def current_edge_set(self):
        if self.is_switched:
            return self.turn
        else:
            return self.straight

    @property
    def point(self):
        if len(self._edges) == 0:
            return None
        elif len(self._edges) <= 2:
            return self._edges[0]
        else:
            norm_vectors = [(n.position - self.position).normalized for n in self.nodes]
            shortest_ids = geometry.shortest_side_of_triangle(norm_vectors)
            other_id = [i for i in range(len(self.nodes)) if i not in shortest_ids][0]
            return self._edges[other_id]
    
    @property
    def straight(self):
        if len(self._edges) < 2:
            return None
        elif len(self._edges) == 2:
            return self._edges[1]
        else:
            norm_vectors = [(n.position - self.position).normalized for n in self.nodes]
            shortest_ids = geometry.shortest_side_of_triangle(norm_vectors)
            point_id = [i for i in range(len(self._edges)) if i not in shortest_ids][0]
            longest_id = geometry.farthest_point(norm_vectors[point_id], [norm_vectors[i] for i in shortest_ids])
            return self._edges[shortest_ids[longest_id]]
    
    @property
    def turn(self):
        if len(self._edges) < 2:
            return None
        elif len(self._edges) == 2:
            return self.straight
        else:
            other_edges = (self.point, self.straight)
            return [e for e in self._edges if e not in other_edges][0]

