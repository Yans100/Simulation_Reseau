import datetime
import sys
from GestionFichiers import GestionFichiers as GF
from paquet.PaquetCommunicationEtablie import PaquetCommunicationEtablie
from CoucheReseau import CoucheReseau
from Reseau import Reseau
from NConnect import NConnect

class CoucheTransport:
    def __init__(self, reseau: Reseau, er: CoucheReseau,
                 s_lec: str = "Files/S_lec.txt",
                 s_ecr: str = "Files/S_ecr.txt") -> None:
        self.reseau = reseau
        self.ER     = er
        self.S_lec  = s_lec
        self.S_ecr  = s_ecr

    def run(self) -> None:
        # 1) Effacer S_ecr.txt
        with open(self.S_ecr, "w", encoding="utf-8"):
            pass

        # 2) Charger tous les messages
        messages = GF.lire_lignes(self.S_lec)
        if not messages:
            return

        # 3) Pour chaque message
        for message in messages:
            src = self.reseau.pick_random_station(-1).adresse
            dst = self.reseau.pick_random_station(src).adresse

            paquet_req = NConnect.demande_connexion(1, src, dst)
            rep = self.ER.demande_de_connexion(paquet_req)

            # a) Timeout
            if rep is None:
                with open(self.S_ecr, "a", encoding="utf-8") as f:
                    f.write("KO 1 - timeout (absence de réponse)\n")

            # b) Refus par le fournisseur ou le destinataire
            elif hasattr(rep, 'raison'):
                if rep.raison == "00000010":
                    with open(self.S_ecr, "a", encoding="utf-8") as f:
                        f.write("KO 1 - refus par le fournisseur\n")
                elif rep.raison == "00000001":
                    with open(self.S_ecr, "a", encoding="utf-8") as f:
                        f.write("KO 1 - refus par le destinataire\n")

            # c) Acceptation
            elif isinstance(rep, PaquetCommunicationEtablie):
                no_conn = int(rep.no_connexion, 2)
                self.ER.envoyer_message(no_conn, message)
                self.ER.liberer(no_conn)
                with open(self.S_ecr, "a", encoding="utf-8") as f:
                    f.write("OK 1 terminé\n")
