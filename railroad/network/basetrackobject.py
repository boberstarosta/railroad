
class BaseTrackObject:

    def __init__(self, network, parent_segment, t, rotated):
        self.network = network
        self._parent_segment = parent_segment
        self._parent_segment.track_objects.append(self)
        self._t = t
        self._rotated = rotated

    def delete(self):
        self._parent_segment.track_objects.remove(self)

    def update(self, dt):
        pass

    def on_parent_segment_changed(self, parent_segment):
        pass

    def on_t_changed(self, t):
        pass

    @property
    def parent_segment(self):
        return self._parent_segment

    @parent_segment.setter
    def parent_segment(self, value):
        if value != self._parent_segment:
            old_parent_segment = self._parent_segment
            self._parent_segment = value
            old_parent_segment.track_objects.remove(self)
            self._parent_segment.track_objects.append(self)

            # Preserve direction if changing to neighboring segment.
            common_node = None
            common_node_old_index = None
            for i, node in enumerate(old_parent_segment.nodes):
                if old_parent_segment.nodes[i].other_segment(old_parent_segment) is value:
                    common_node = node
                    common_node_old_index = i
                    break
            if common_node is not None:
                common_node_new_index = value.nodes.index(common_node)
                if common_node_old_index == common_node_new_index:
                    self.rotated = not self.rotated

            self.on_parent_segment_changed(self._parent_segment)

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        if value != self._t:
            self._t = value
            self.on_t_changed(value)

    def on_rotated_changed(self, rotated):
        pass

    @property
    def rotated(self):
        return self._rotated

    @rotated.setter
    def rotated(self, value):
        if value != self._rotated:
            self._rotated = value
            self.on_rotated_changed(value)

