from .Paquet import Paquet

class PaquetDonnees(Paquet):
    def __init__(self, no_connexion: str, donnees: str):
        super().__init__(no_connexion)
        self.__donnees = donnees
        self.__type = ""

    # Getters/Setters
    @property
    def donnees(self) -> str:
        return self.__donnees

    @donnees.setter
    def donnees(self, value: str):
        self.__donnees = value

    #Méthode toString
    def __str__(self) -> str:
        return f"{super().__str__()}\n{self.__donnees}"