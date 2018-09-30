
from ..vec import Vec
from .node import Node
from .edge import Edge
from .signal import Signal
from .blocksignal import BlockSignal
from .distantsignal import DistantSignal
from .opentrackmarker import OpenTrackMarker


str_to_type = {
    "S": Signal,
    "BS": BlockSignal,
    "DS": DistantSignal,
    "OTM": OpenTrackMarker,
}

type_to_str = {v: k for k, v in str_to_type.items()}


def save_network(network, filename):
    lines = []

    for node in network.nodes:
        symbol = "N"
        pos = "{},{}".format(node.position.x, node.position.y)
        lines.append("|".join((symbol, pos)))

    for edge in network.edges:
        symbol = "E"
        nodes = ",".join([str(network.nodes.index(n)) for n in edge.nodes])
        straight = str(edge.straight)
        lines.append("|".join((symbol, nodes, straight)))

    with open(filename, mode="w") as f:
        f.write("\n".join(lines))

def load_network(network, filename):
    while len(network.edges) > 0:
        network.edges[-1].delete()
    while len(network.nodes) > 0:
        network.nodes[-1].delete()

    node_records = []
    edge_records = []

    with open(filename, mode="r") as f:
        for line in f.readlines():
            words = line.strip().split("|")
            symbol, data = words[0], words[1:]
            if symbol == "N":
                node_records.append(data)
            elif symbol == "E":
                edge_records.append(data)

    for record in node_records:
        str_pos = record[0]
        pos = Vec([float(s) for s in str_pos.split(",")])
        Node(network, pos)

    for str_nodes, str_straight in edge_records:
        str_node_indices = str_nodes.split(",")
        node1, node2 = [network.nodes[int(i)] for i in str_node_indices]
        straight = str_straight == "True"
        Edge(network, node1, node2, straight)
