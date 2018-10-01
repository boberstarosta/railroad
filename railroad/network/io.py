
from ..vec import Vec
from .node import Node
from .edge import Edge
from .signal import Signal
from .blocksignal import BlockSignal
from .distantsignal import DistantSignal
from .opentrackmarker import OpenTrackMarker
from .sceneryobject import SceneryObject


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
        switched = str(node.is_switched)
        lines.append("|".join((symbol, pos, switched)))

    for edge in network.edges:
        symbol = "E"
        nodes = ",".join([str(network.nodes.index(n)) for n in edge.nodes])
        straight = str(edge.straight)
        lines.append("|".join((symbol, nodes, straight)))

    for to in network.track_objects:
        symbol = "TO"
        type_ = type_to_str[type(to)]
        parent_edge = str(network.edges.index(to.parent_segment.parent_edge))
        parent_segment_index = str(to.parent_segment.parent_edge.track_segments.index(to.parent_segment))
        t = str(to.t)
        rotated = str(to.rotated)
        lines.append("|".join((symbol, type_, parent_edge, parent_segment_index, t, rotated)))

    for so in network.scenery_objects:
        symbol = "SO"
        pos = "{},{}".format(so.position.x, so.position.y)
        rotation = str(so.rotation)
        lines.append("|".join((symbol, pos, rotation)))

    with open(filename, mode="w") as f:
        f.write("\n".join(lines))

def load_network(network, filename):
    # Clear the network - edges, nodes, track objects
    while len(network.edges) > 0:
        network.edges[-1].delete()
    while len(network.nodes) > 0:
        network.nodes[-1].delete()
    while len(network.scenery_objects) > 0:
        network.scenery_objects[-1].delete()

    # Clear all trains - traincars, consists
    while len(network.app.trains.traincars) > 0:
        network.app.trains.traincars[-1].delete()
    while len(network.app.trains.consists) > 0:
        network.app.trains.consists[-1].delete()

    node_records = []
    edge_records = []
    to_records = []
    so_records = []
    nodes_to_switch = []

    with open(filename, mode="r") as f:
        for line in f.readlines():
            words = line.strip().split("|")
            symbol, data = words[0], words[1:]
            if symbol == "N":
                node_records.append(data)
            elif symbol == "E":
                edge_records.append(data)
            elif symbol == "TO":
                to_records.append(data)
            elif symbol == "SO":
                so_records.append(data)

    for str_pos, str_switched in node_records:
        pos = Vec([float(s) for s in str_pos.split(",")])
        switched = str_switched == "True"
        node = Node(network, pos)
        if switched:
            nodes_to_switch.append(node)

    for str_nodes, str_straight in edge_records:
        str_node_indices = str_nodes.split(",")
        node1, node2 = [network.nodes[int(i)] for i in str_node_indices]
        straight = str_straight == "True"
        Edge(network, node1, node2, straight)

    for s_type, s_edge, s_segment_index, s_t, s_rot in to_records:
        type_ = str_to_type[s_type]
        edge = network.edges[int(s_edge)]
        parent_segment = edge.track_segments[int(s_segment_index)]
        t = float(s_t)
        rotated = s_rot == "True"
        type_(network, parent_segment, t, rotated=rotated)

    for s_position, s_rotation in so_records:
        position = Vec([float(s) for s in s_position.split(",")])
        rotation = float(s_rotation)
        SceneryObject(network, position, rotation)

    for node in nodes_to_switch:
        node.switch()
