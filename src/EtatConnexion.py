from enum import Enum

class EtatConnexion(Enum):
    ATTENTE = "En attente de connexion"
    CONNEXION_ETABLIE = "Connexion établie"

    def __str__(self):
        return self.value
