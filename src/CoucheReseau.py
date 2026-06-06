import random, time
from typing import List, Optional
from paquet.Paquet import Paquet
from paquet.PaquetAdresse import PaquetAdresse
from paquet.PaquetCommunicationEtablie import PaquetCommunicationEtablie
from paquet.PaquetDonnees import PaquetDonnees
from NConnect import NConnect
from NDisconnect import NDisconnect
from GestionFichiers import GestionFichiers
from EtatConnexion import EtatConnexion
from Connexion import Connexion
from Reseau import Reseau

TAILLE_MAX_PAQUET = 128

class CoucheReseau:
    def __init__(self, reseau: 'Reseau', path_L_ecr: str, path_L_lec: str):
        self.reseau       = reseau
        self.path_L_ecr   = path_L_ecr
        self.path_L_lec   = path_L_lec
        self.etat_connexion = EtatConnexion.ATTENTE
        self.connexion      = None
        self.no_connexion   = 0

    def demande_de_connexion(self, paquet_demande_conn: PaquetAdresse) -> Optional[Paquet]:
        source      = int(paquet_demande_conn.adr_source, 2)
        destination = int(paquet_demande_conn.adr_destination, 2)

        # 1) Refus par le fournisseur (source multiple de 27) → KO
        if not self.decision_connexion_par_er(source):
            return self.refuser_connexion(paquet_demande_conn)

        # 2) Poursuite de l’établissement
        self.connexion = self.ajouter_connexion(source, destination)
        paquet = self.former_paquet_d_appel(self.connexion)
        self.ecrire_dans_fichier_liaison(str(paquet))

        # 3) Gestion de la réponse distante
        return self.reponse_demande_de_connexion_dist(self.connexion)

    @staticmethod
    def decision_connexion_par_er(source: int) -> bool:
        return source % 27 != 0

    def refuser_connexion(self, paquet_demande_conn: PaquetAdresse) -> Paquet:
        no_conn = int(paquet_demande_conn.no_connexion, 2)
        src     = int(paquet_demande_conn.adr_source,      2)
        dst     = int(paquet_demande_conn.adr_destination, 2)
        self.connexion = None
        self.etat_connexion = EtatConnexion.ATTENTE
        return NDisconnect.ind_values(no_conn, src, dst, "00000010")

    def ajouter_connexion(self, source_add: int, destination_add: int):
        source = self.reseau.get_station(source_add)
        destination = self.reseau.get_station(destination_add)
        self.no_connexion += 1
        return Connexion(self.no_connexion, source, destination)

    @staticmethod
    def former_paquet_d_appel(connexion: 'Connexion') -> Paquet:
        return NConnect.indication_connexion(connexion)

    def reponse_demande_de_connexion_dist(self, connexion: 'Connexion') -> Optional[Paquet]:
        source = connexion.source.adresse

        # a) Timeout (pas de réponse) si multiple de 19
        if source % 19 == 0:
            return None

        # b) Refus par le destinataire (multiple de 13)
        if source % 13 == 0:
            return self.refuser_connexion_du_destinataire(connexion)

        # c) Acceptation
        return self.accepter_connexion(connexion)

    def refuser_connexion_du_destinataire(self, connexion: 'Connexion') -> Paquet:
        paquet_ind = NDisconnect.ind(connexion, "00000001")
        self.connexion = None
        self.etat_connexion = EtatConnexion.ATTENTE
        return paquet_ind

    def accepter_connexion(self, connexion: 'Connexion') -> Paquet:
        paquet_conf = NConnect.confirmation(connexion)
        self.etat_connexion = EtatConnexion.CONNEXION_ETABLIE
        if paquet_conf.type == "00001111":
            self.ecrire_a_lire(str(paquet_conf))
        return paquet_conf

    def ecrire_dans_fichier_liaison(self, message: str):
        with open(self.path_L_ecr, "a", encoding="utf-8") as f:
            f.write(message.rstrip("\n") + "\n")

    def ecrire_a_lire(self, message: str) -> None:
        with open(self.path_L_lec, "a", encoding="utf-8") as f:
            f.write(message.rstrip("\n") + "\n")

    def envoyer_message(self, no_connexion: int, message: str):
        # Construction des paquets de données à partir du message (découpage si nécessaire)
        paquets = self.construire_paquets(message, no_connexion)

        # Parcours de chaque paquet à envoyer
        for p in paquets:
            # Écriture du paquet de données dans L_ecr.txt (côté émission)
            self.ecrire_dans_fichier_liaison(str(p))
            time.sleep(0.05)  # Petite pause pour simuler le délai réseau

            # --- Simulation de la réponse de la couche liaison ---
            source_addr = self.connexion.source.adresse

            # 1) Si l'adresse source est un multiple de 15, on simule un timeout : aucun acquittement n'est généré
            if source_addr % 15 == 0:
                continue  # On passe au paquet suivant sans écrire dans L_lec.txt

            # 2) Sinon, on simule un acquittement (ACK ou NACK) aléatoire
            ack_type = self.simuler_acquittement()

            # 3) Écriture de l'acquittement dans L_lec.txt (côté réception)
            # Chaque acquittement est préfixé par le numéro de connexion
            ack_message = f"{p.no_connexion}\n{ack_type}"
            self.ecrire_a_lire(ack_message)

    def simuler_acquittement(self) -> str:
        # Simuler un acquittement positif ("00000001") ou négatif ("00000101")
        import random
        return "00000001" if random.random() < 0.8 else "00000101"  # 80% chance de ACK

    def liberer(self, no_connexion: int):
        src_addr = self.connexion.source.adresse
        dst_addr = self.connexion.destination.adresse
        paquet_demande = NDisconnect.req_values(no_connexion, src_addr, dst_addr)
        self.ecrire_dans_fichier_liaison(str(paquet_demande))
        self.etat_connexion = EtatConnexion.ATTENTE

    def construire_paquets(self, message: str, no_connexion: int) -> List[PaquetDonnees]:
        if not isinstance(message, str) or not isinstance(no_connexion, int) or no_connexion < 0:
            raise ValueError("Paramètres invalides")

        paquets = []
        no_connexion_bin = self.to_eight_bits(no_connexion)

        if len(message) > TAILLE_MAX_PAQUET:
            for i in range(0, len(message), TAILLE_MAX_PAQUET):
                chunk = message[i:i + TAILLE_MAX_PAQUET]
                paquet = PaquetDonnees(no_connexion_bin, chunk)
                paquet.type = "00000000"
                paquets.append(paquet)
        else:
            paquet = PaquetDonnees(no_connexion_bin, message)
            paquet.type = "00000000"
            paquets.append(paquet)

        return paquets

    @staticmethod
    def to_eight_bits(value: int) -> str:
        return f"{value:08b}"
