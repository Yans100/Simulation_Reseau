from .Paquet import Paquet

class PaquetAcquittement(Paquet):
    def __init__(self, no_connexion: str):
        super().__init__(no_connexion)

    def __str__(self) -> str:
        return super().__str__()