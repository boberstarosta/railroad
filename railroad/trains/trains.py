
class Trains:

    def __init__(self, network):
        self.network = network
        self.consists = []
        self.traincars = []

    def update(self, dt):
        for consist in self.consists:
            consist.update(dt)
