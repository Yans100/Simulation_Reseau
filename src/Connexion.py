from EtatConnexion import EtatConnexion
from Station import Station

class Connexion:
    def __init__(self, no_demande: int, source: 'Station', destination: 'Station'):
        self.__no_connexion = no_demande
        self.__source = source
        self.__destination = destination
        self.__etat_connexion = EtatConnexion.ATTENTE

    @property
    def source(self) -> 'Station':
        return self.__source

    @source.setter
    def source(self, value: 'Station') -> None:
        self.__source = value

    @property
    def destination(self) -> 'Station':
        return self.__destination

    @destination.setter
    def destination(self, value: 'Station') -> None:
        self.__destination = value

    @property
    def etat_connexion(self) -> 'EtatConnexion':
        return self.__etat_connexion

    @etat_connexion.setter
    def etat_connexion(self, etat: 'EtatConnexion') -> None:
        self.__etat_connexion = etat

    @property
    def no_connexion(self) -> int:
        return self.__no_connexion

    @no_connexion.setter
    def no_connexion(self, no: int) -> None:
        self.__no_connexion = no

    # Méthode toString
    def __str__(self) -> str:
        return (f"Connexion(no={self.__no_connexion}, "
                f"src={self.__source}, "
                f"dest={self.__destination})")

