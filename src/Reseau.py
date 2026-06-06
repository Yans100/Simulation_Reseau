import random
from Station import Station

class Reseau:
    """Maintient les 255 stations disponibles."""
    def __init__(self):
        self.stations = [Station(i) for i in range(255)]

    def get_station(self, addr: int) -> Station:
        return self.stations[addr]

    def pick_random_station(self, exclude: int) -> Station:
        addr = exclude
        while addr == exclude:
            addr = random.randint(0, 254)
        return self.get_station(addr)

    def get_one_random_station(self, exclude: int):
        return self.pick_random_station(exclude)
