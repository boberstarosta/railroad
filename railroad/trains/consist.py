
class Consist:

    def __init__(self, trains):
        self.trains = trains
        self.traincars = []
        self.velocity = -500
        trains.consists.append(self)

    def delete(self):
        while len(self.traincars) > 0:
            self.traincars[-1].delete()
        self.trains.consists.remove(self)

    def update(self, dt):
        for traincar in self.traincars:
            traincar.update_velocity(dt, self.velocity)

    @property
    def engine_count(self):
        return len([tc for tc in self.traincars if tc.model.has_engine])

    @property
    def mass(self):
        return sum(tc.model.mass for tc in self.traincars)
