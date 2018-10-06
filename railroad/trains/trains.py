
class Trains:

    def __init__(self, network):
        self.network = network
        self.traincars = []
        self.consists = []

    def update(self, dt):
        for consist in self.consists:
            consist.update(dt)
