from EtatConnexion import EtatConnexion
from typing import Final


class Station:
    """Représente une station réseau avec son adresse et son état de connexion."""

    def __init__(self, adresse: int) -> None:
        """
        Initialise une nouvelle station.

        Args:
            adresse: L'adresse numérique unique de la station
        """
        self.__adresse: Final[int] = adresse  # Immutable après initialisation
        self.__etat_connexion: EtatConnexion = EtatConnexion.ATTENTE

    @property
    def adresse(self) -> int:
        """L'adresse réseau de la station (en lecture seule)."""
        return self.__adresse

    @property
    def etat_connexion(self) -> EtatConnexion:
        """L'état actuel de la connexion."""
        return self.__etat_connexion

    @etat_connexion.setter
    def etat_connexion(self, valeur: EtatConnexion) -> None:
        """
        Modifie l'état de connexion.

        Args:
            valeur: Nouvel état (doit être membre de EtatConnexion)

        Raises:
            TypeError: Si la valeur n'est pas un EtatConnexion valide
        """
        if not isinstance(valeur, EtatConnexion):
            raise TypeError(f"L'état doit être de type EtatConnexion, pas {type(valeur).__name__}")
        self.__etat_connexion = valeur

    def __repr__(self) -> str:
        return f"Station(adresse={self.__adresse}, etat={self.__etat_connexion.name})"