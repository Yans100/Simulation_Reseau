from .PaquetAdresse import PaquetAdresse
from .Paquet import Paquet

class PaquetCommunicationEtablie(PaquetAdresse):
    def __init__(self, no_connexion: str, adr_source: str, adr_destination: str):
        super().__init__(no_connexion, adr_source, adr_destination)
        self.type = "00001111"

    def __str__(self):
        return (
            f"{self.no_connexion}\n"
            f"{self.type}\n"
            f"{self.adr_source}\n"
            f"{self.adr_destination}"
        )

