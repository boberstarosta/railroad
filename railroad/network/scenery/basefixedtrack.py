
from .basesceneryobject import BaseSceneryObject
from ..node import Node
from ..edge import Edge
from railroad.vec import Vec


class BaseFixedTrack(BaseSceneryObject):

    image = None

    def __init__(self, network, position, rel_node_positions, connection_indices, rotation=0):
        super().__init__(network, position, rotation)
        # TODO: Transform relative node positions to get absolute positions.
        absolute_node_positions = [p for p in rel_node_positions]
        self.nodes = [Node(network, pos) for pos in absolute_node_positions]
        self.edges = [Edge(network, self.nodes[i0], self.nodes[i1], True) for i0, i1 in connection_indices]

    def delete(self):
        for edge in self.edges:
            edge.delete()
        for node in self.nodes:
            node.delete()
        super().delete()

    def on_position_changed(self, position):
        pass

    def on_rotation_changed(self, rotation):
        pass