
class Trains:

    def __init__(self, network):
        self.network = network
        self.traincars = []

    def update(self, dt):
        for traincar in self.traincars:
            traincar.update(dt)
