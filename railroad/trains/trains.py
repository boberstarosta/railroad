
class Trains:

    def __init__(self, network):
        self.network = network
        self.consists = []
        self.traincars = []
        self.couplings = []

    def update(self, dt):
        for consist in self.consists:
            consist.update(dt)

    def nearest_coupling(self, position, traincar=None):
        nearest_coupling = None
        shortest_distance_sq = float("inf")
        for coupling in [c for c in self.couplings if traincar is None or traincar in c.traincars]:
            distance_sq = (coupling.position - position).length_sq
            if distance_sq < shortest_distance_sq:
                shortest_distance_sq = distance_sq
                nearest_coupling = coupling
        return nearest_coupling
