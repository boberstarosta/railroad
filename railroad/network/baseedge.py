
class BaseEdge:
    
    @classmethod
    def is_possible(self, node1, node2):
        different = node1 is not node2
        not_connected = not node1.is_connected(node2)
        have_free_connections = node1.has_free_connections and node2.has_free_connections
        return different and not_connected and have_free_connections
    
    def __init__(self, node1, node2):
        if not self.__class__.is_possible(node1, node2):
            raise ValueError("Impossible to connect")
        self._nodes = node1, node2
        for node in self._nodes:
            node.add_edge(self)
    
    @property
    def nodes(self):
        return list(self._nodes)
    
    def delete(self):
        for node in self.nodes:
            node.remove_edge(self)
    
    def other_node(self, node):
        if self.nodes[0] is node:
            return self.nodes[1]
        elif self.nodes[1] is node:
            return self.nodes[0]
        else:
            raise IndexError("Edge.other_node: Not my node")
    
    @property
    def length(self):
        return (self.nodes[1].position - self.nodes[0].position).length
    
    @property
    def direction(self):
        return (self._nodes[1].position - self._nodes[0].position).normalized

