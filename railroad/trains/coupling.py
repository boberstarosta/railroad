
import pyglet
from .. import graphics


class Coupling:

    length = 150

    def __init__(self, *traincars):
        self.traincars = traincars
        self.sprite = pyglet.sprite.Sprite(
            graphics.img.coupling,
            group=graphics.group.couplings,
            batch=traincars[0].trains.network.app.batch
        )
        self.sprite.scale = self.length / self.sprite.width
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

        directions = [None]*len(self.traincars)
        for i, (tc, other_index) in enumerate(zip(self.traincars, tc_indices)):
            directions[i] = tc.direction if other_index == 1 else -tc.direction

        tc_ends = [tc.position + tc.direction*tc.model.length/2 for tc in self.traincars]

        self.sprite.position = (tc_ends[0] + tc_ends[1]) / 2
        self.sprite.rotation = -(tc_ends[1] - tc_ends[0]).angle

        # Debugging
        self.sprite.position = (self.traincars[1].position + self.traincars[0].position)/2

        print("Coupling.update_sprite {}".format(self.sprite.position))
