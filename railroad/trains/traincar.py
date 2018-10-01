
class TrainCar:

    def __init__(self, trains, model, parent_segment, t, rotated=False, parent_consist=None):
        self.trains = trains
        self.model = model
        self.parent_segment = parent_segment
        self._t = t
        self._rotated = rotated
        self.parent_consist = parent_consist
        self.sprite = model.create_sprite(trains.network.app.batch)
        trains.traincars.append(self)
        self._update_sprite()

    def delete(self):
        self.sprite.delete()
        self.trains.traincars.remove(self)

    def update(self, dt):
        pass

    def _update_sprite(self):
        vector = self.parent_segment.nodes[1].position - self.parent_segment.nodes[0].position
        self.sprite.position = self.parent_segment.nodes[0].position + vector * self.t
        self.sprite.rotation = -vector.angle

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        if value != self._t:
            self._t = value
            self._update_sprite()
