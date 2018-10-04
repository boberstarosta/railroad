
class Coupling:

    length = 50

    def __init__(self, trains, traincar):
        self.trains = trains
        self.traincars = [traincar]
        trains.couplings.append(self)

    def delete(self):
        self.trains.couplings.remove(self)

    @property
    def position(self):
        if self is self.traincars[0].couplings[0]:
            direction = -self.traincars[0].direction
        else:
            direction = self.traincars[0].direction
        return self.traincars[0].position + direction * self.traincars[0].model.length / 2
