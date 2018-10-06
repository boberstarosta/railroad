
from .basesceneryobject import BaseSceneryObject
from ..node import Node
from ..edge import Edge
from railroad.vec import Vec


class BaseFixedTrack(BaseSceneryObject):

    image = None

    def __init__(self, network, position, rel_node_positions, connection_indices, rotation=0):
        super().__init__(network, position, rotation)
        self._relative_node_positions = rel_node_positions
        self._nodes = [Node(network, Vec()) for _ in rel_node_positions]
        self._edges = [Edge(network, self._nodes[i0], self._nodes[i1], True) for i0, i1 in connection_indices]
        self._update_node_positions()

    def delete(self):
        for edge in self._edges:
            edge.delete()
        for node in self._nodes:
            node.delete()
        super().delete()

    def on_position_changed(self, position):
        self._update_node_positions()

    def on_rotation_changed(self, rotation):
        self._update_node_positions()

    def _update_node_positions(self):
        for rel_pos, node in zip(self._relative_node_positions, self._nodes):
            node.position = rel_pos.rotated(self.rotation)
