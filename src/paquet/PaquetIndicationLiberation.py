from .PaquetAdresse import PaquetAdresse

class PaquetIndicationLiberation(PaquetAdresse):
    def __init__(self, no_connexion: str, adr_source: str, adr_destination: str, raison: str):
        super().__init__(no_connexion, adr_source, adr_destination)

        self.__raison = raison
        self.type = "00010011"

    # Getters/Setters
    @property
    def raison(self) -> str:
        return self.__raison

    @raison.setter
    def raison(self, value: str):
        self.__raison = value

    # Méthode toString
    def __str__(self) -> str:
        # super().__str__() affiche déjà no_connexion, type, adr_source et adr_destination
        return f"{super().__str__()}\n{self.raison}"