from abc import ABC

class Paquet(ABC):
    #Attributs de la classe parent
    def __init__(self, no_connexion: str):
        self.__no_connexion = no_connexion
        self.__type = ""

    # Getters et Setters pour un accès contrôlé à nos attributs
    @property
    def no_connexion(self) -> str:
        return self.__no_connexion

    @no_connexion.setter
    def no_connexion(self, value: str):
        self.__no_connexion = value

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    # Méthode toString
    def __str__(self) -> str:
        return f"{self.__no_connexion}\n{self.__type}"
