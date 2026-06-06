from abc import ABC
from .Paquet import Paquet

class PaquetAdresse(Paquet, ABC):
    def __init__(self, no_connexion: str, adr_source: str, adr_destination: str):
        super().__init__(no_connexion)
        self.__adr_source = adr_source
        self.__adr_destination = adr_destination

    @property
    def adr_source(self) -> str:
        return self.__adr_source

    @adr_source.setter
    def adr_source(self, value: str):
        self.__adr_source = value

    @property
    def adr_destination(self) -> str:
        return self.__adr_destination

    @adr_destination.setter
    def adr_destination(self, value: str):
        self.__adr_destination = value

    def __str__(self) -> str:
        return f"{super().__str__()}\n{self.__adr_source}\n{self.__adr_destination}"
