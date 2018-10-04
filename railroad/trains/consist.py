
class Consist:

    def __init__(self, trains):
        self.trains = trains
        self.traincars = []
        trains.consists.append(self)

    def delete(self):
        for traincar in self.traincars:
            traincar.delete()
        self.trains.consists.remove(self)

    def update(self, dt):
        for traincar in self.traincars:
            traincar.update(dt)
