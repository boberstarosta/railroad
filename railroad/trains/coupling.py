
import pyglet
from .. import graphics


class Coupling:

    length = 50

    def __init__(self, *traincars):
        self.traincars = traincars
        self.sprite = pyglet.sprite.Sprite(
            graphics.img.coupling,
            group=graphics.group.couplings,
            batch=traincars[0].trains.network.app.batch
        )
        self.sprite.scale = 3*self.length / self.sprite.width
        for traincar in self.traincars:
            traincar.couplings.append(self)
        self.update_sprite()

    def delete(self):
        self.sprite.delete()
        for traincar in self.traincars:
            traincar.couplings.remove(self)

    def update_sprite(self):
        tc_indices = [None]*len(self.traincars)
        for i, tc in enumerate(self.traincars):
            other_tc = self.traincars[(i + 1)%len(self.traincars)]
            tc_indices[i] = tc.coupled_traincars.index(other_tc)

        positions = [tc.wheels[tc_indices[i]].position for i, tc in enumerate(self.traincars)]

        self.sprite.position = (positions[0] + positions[1]) / 2
        self.sprite.rotation = -(positions[1] - positions[0]).angle
