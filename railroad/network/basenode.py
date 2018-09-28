
from .. import geometry


class BaseNode:

    max_connections = 3
    
    def __init__(self, position):
        self._edges = []
        self._position = position
    
    def delete(self):
        pass
    
    def add_edge(self, edge):
        if len(self._edges) < self.max_connections:
            self._edges.append(edge)
        else:
            raise ValueError("Node.add_edge: Too many connections")
    
    def remove_edge(self, edge):
        self._edges.remove(edge)
    
    def on_position_changed(self, position): pass
    
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        if value != self._position:
            self._position = value
            self.on_position_changed(value)

    @property
    def edges(self):
        return list(self._edges)
    
    @property
    def connected_nodes(self):
        return [edge.other_node(self) for edge in self._edges]
    
    def is_connected(self, other):
        return other in self.connected_nodes
    
    def other_edges(self, edge):
        if edge not in self._edges:
            raise ValueError("BaseNode.other_edges: Not my edge")
        return [e for e in self._edges if e is not edge]
    
    @property
    def has_free_connections(self):
        return len(self._edges) < self.max_connections
    
    @property
    def nodes(self):
        return [e.other_node(self) for e in self._edges]

