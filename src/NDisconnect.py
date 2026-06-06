from paquet.PaquetDemandeLiberation import PaquetDemandeLiberation
from paquet.PaquetIndicationLiberation import PaquetIndicationLiberation



class NDisconnect:
    @staticmethod
    def req(connexion):
        return PaquetDemandeLiberation(
            NDisconnect._to_eight_bits(connexion.no_connexion),
            NDisconnect._to_eight_bits(connexion.source.adresse),
            NDisconnect._to_eight_bits(connexion.destination.adresse)
        )

    @staticmethod
    def req_values(no_connexion, source, destination):
        return PaquetDemandeLiberation(
            NDisconnect._to_eight_bits(no_connexion),
            NDisconnect._to_eight_bits(source),
            NDisconnect._to_eight_bits(destination)
        )

    @staticmethod
    def ind(connexion, raison):
        return PaquetIndicationLiberation(
            NDisconnect._to_eight_bits(connexion.no_connexion),
            NDisconnect._to_eight_bits(connexion.source.adresse),
            NDisconnect._to_eight_bits(connexion.destination.adresse),
            raison
        )

    @staticmethod
    def ind_values(no_connexion, source, destination, raison):
        return PaquetIndicationLiberation(
            NDisconnect._to_eight_bits(no_connexion),
            NDisconnect._to_eight_bits(source),
            NDisconnect._to_eight_bits(destination),
            raison
        )

    @staticmethod
    def ind_simple(no_connexion, source, destination):
        return PaquetDemandeLiberation(
            NDisconnect._to_eight_bits(no_connexion),
            NDisconnect._to_eight_bits(source),
            NDisconnect._to_eight_bits(destination)
        )

    @staticmethod
    def _to_eight_bits(value):
        return bin(value)[2:].zfill(8)
