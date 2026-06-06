from .PaquetAdresse import PaquetAdresse

class PaquetDemandeLiberation(PaquetAdresse):
    def __init__(self, no_connexion: str, adr_source: str, adr_destination: str):
        super().__init__(no_connexion, adr_source, adr_destination)

        self.type = "00010011"
