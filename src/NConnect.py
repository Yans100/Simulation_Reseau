from paquet.PaquetAppel import PaquetAppel
from paquet.PaquetCommunicationEtablie import PaquetCommunicationEtablie
from Connexion import Connexion

class NConnect:
    @staticmethod
    def demande_connexion(no_demande: int, source: int, destination: int) -> 'PaquetAppel':
        """Demande de connexion au réseau"""
        no_dem = NConnect.to_eight_bits(no_demande)
        source_bin = NConnect.to_eight_bits(source)
        dest_bin = NConnect.to_eight_bits(destination)

        return PaquetAppel(no_dem, source_bin, dest_bin)

    @staticmethod
    def indication_connexion(connexion: Connexion) -> PaquetAppel:
        """Indication de connexion au réseau"""
        no_demande = NConnect.to_eight_bits(connexion.no_connexion)
        source = NConnect.to_eight_bits(connexion.source.adresse)
        destination = NConnect.to_eight_bits(connexion.destination.adresse)

        return PaquetAppel(no_demande, source, destination)


    @staticmethod
    def reponse(connexion: Connexion) -> PaquetCommunicationEtablie:
        """Réponse à une demande de connexion"""
        return NConnect.confirmation(connexion)

    @staticmethod
    def confirmation(connexion: Connexion) -> PaquetCommunicationEtablie:
        """Confirmation de connexion"""
        return PaquetCommunicationEtablie(
            NConnect.to_eight_bits(connexion.no_connexion),
            NConnect.to_eight_bits(connexion.source.adresse),
            NConnect.to_eight_bits(connexion.destination.adresse)
        )

    @staticmethod
    def to_eight_bits(value: int) -> str:
        """Convertit une valeur en binaire sur 8 bits (ajoute des zéros si nécessaire)"""
        return f"{value:08b}"
