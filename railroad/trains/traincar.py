
class TrainCar:

    def __init__(self, trains, model):
        self.trains = trains
        self.model = model
        self.sprite = model.create_sprite()
        trains.traincars.append(self)

    def delete(self):
        self.sprite.delete()
        self.trains.traincars.remove(self)
