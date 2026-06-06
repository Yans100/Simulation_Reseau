# =============================================================
# File: SimGUI.py
# -------------------------------------------------------------
"""
Interface graphique (Tkinter) pour piloter la simulation réseau‑transport
existante (CoucheTransport / CoucheReseau) et visualiser les trois phases
comme dans le prototype « AvecAnimation.py ».

• On conserve 100 % du backend Python que tu as déjà corrigé.
  (Main.py, CoucheTransport.py, CoucheReseau.py, etc.)

• Cette interface se contente d'appeler les méthodes publiques du backend
  et d'afficher, animer les échanges.

Utilisation :
    python SimGUI.py

Prérequis : le dossier Files/ doit exister (ou laisser l'appli le créer).
"""

import tkinter as tk
from tkinter import messagebox
import time
import datetime
import random
from pathlib import Path

# --- backend projet -------------------------------
from Reseau import Reseau
from CoucheTransport import CoucheTransport
from CoucheReseau import CoucheReseau
from GestionFichiers import GestionFichiers as GF

FILES_DIR = Path("Files")
S_LEC      = FILES_DIR / "S_lec.txt"
S_ECR      = FILES_DIR / "S_ecr.txt"
L_ECR      = FILES_DIR / "L_ecr.txt"
L_LEC      = FILES_DIR / "L_lec.txt"


class ReseauSimGUI(tk.Tk):
    """Fenêtre principale"""
    def __init__(self):
        super().__init__()
        self.title("Simulation Réseau Connecté – GUI")
        self.geometry("900x540")
        self.resizable(False, False)

        # --- backend -----------------------------------------------------
        self.reseau = Reseau()
        # on instancie CoucheReseau indépendamment ; CoucheTransport en reçoit la ref plus tard
        self.ER = CoucheReseau(self.reseau, str(L_ECR), str(L_LEC))
        self.ET = CoucheTransport(self.reseau, self.ER, s_lec=str(S_LEC), s_ecr=str(S_ECR))

        # log fichier écran
        self.logfile = FILES_DIR / "gui_log.txt"
        # réinitialiser gui_log, L_ecr et L_lec
        self.logfile.write_text("--- Lancement GUI ---\n", encoding="utf-8")
        L_ECR.write_text("", encoding="utf-8")
        L_LEC.write_text("", encoding="utf-8")
        # --- Initialisation des attributs ---
        self.rep_er = None    # recevra le paquet de réponse d'établissement
        self.src = None       # adresse source en int
        self.dst = None       # adresse destination en int
        # état
        self.phase = 0  # 0 : pas démarré
        self.no_connexion_actuelle = None
        self.msg_file_idx = 0  # ligne en cours dans S_lec

        # --- UI -----------------------------------------------------------
        self._build_ui()

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
    def _build_ui(self):
        # Bandeau visuel réseau
        self.canvas = tk.Canvas(self, width=860, height=170, bg="white")
        self.canvas.pack(pady=10)
        self._draw_network()

        # zone log
        self.txt = tk.Text(self, height=14, width=110)
        self.txt.pack(pady=6)
        self.txt.config(state=tk.DISABLED)

        # entrée message + boutons
        frm = tk.Frame(self)
        frm.pack()
        self.entry = tk.Entry(frm, width=45, state=tk.DISABLED)
        self.entry.grid(row=0, column=0, padx=5)
        self.btn_send = tk.Button(frm, text="Envoyer", command=self._send_data, state=tk.DISABLED)
        self.btn_send.grid(row=0, column=1, padx=5)
        self.btn_next = tk.Button(self, text="Démarrer la simulation", command=self._next_phase)
        self.btn_next.pack(pady=8)

    def _draw_network(self):
        self.canvas.delete("all")
        self.canvas.create_oval(50, 60, 150, 120, fill="#cce5ff", outline="black")
        self.canvas.create_text(100, 90, text="Système A")
        self.canvas.create_oval(710, 60, 810, 120, fill="#d4edda", outline="black")
        self.canvas.create_text(760, 90, text="Système B")
        self.arrow = self.canvas.create_line(150, 90, 710, 90, arrow=tk.LAST, width=2)

    # ------------------------------------------------------------------
    # logging & animation
    # ------------------------------------------------------------------
    def _log(self, msg: str):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        line = f"{timestamp} {msg}\n"
        self.logfile.write_text(self.logfile.read_text(encoding="utf-8") + line, encoding="utf-8")
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, line)
        self.txt.yview(tk.END)
        self.txt.config(state=tk.DISABLED)

    def _animate_arrow(self, direction="AtoB", steps: int = 24):
        dx = (560 // steps)  # distance horizontale
        for i in range(steps):
            x1 = 150 + dx * i if direction == "AtoB" else 710 - dx * i
            x2 = x1 + 1 if direction == "AtoB" else x1 - 1
            self.canvas.coords(self.arrow, x1, 90, x2, 90)
            self.update()
            time.sleep(0.01)

    def _bubble(self, text: str, direction="AtoB"):
        start_x = 150 if direction == "AtoB" else 710
        dx = +22 if direction == "AtoB" else -22
        bubble = self.canvas.create_text(start_x, 40, text=text, tags="bubble")
        for _ in range(20):
            self.canvas.move(bubble, dx, 0)
            self.update()
            time.sleep(0.05)
        self.canvas.delete(bubble)

    # ------------------------------------------------------------------
    # Phases
    # ------------------------------------------------------------------
    def _next_phase(self):
        if self.phase == 0:
            self._etablissement()
            self._choix_connexion()

            # Si le bouton est désactivé (refus ou timeout), on bloque immédiatement
            if self.btn_next['state'] == tk.DISABLED:
                return

            if self.rep_er is None:
                return

            if self.no_connexion_actuelle is not None:
                self.phase = 2
                self.btn_next.config(text="Commencer transfert")
            return

        elif self.phase == 2:
            self.btn_next.config(text="Libérer connexion")
            self._transfert()
            self.phase = 3
            return

        elif self.phase == 3:
            self.btn_next.config(text="Terminer session")
            self._liberation()
            self.phase = 4
            return

        else:
            self._log("--- Fin de session ---")
            self.btn_next.config(state=tk.DISABLED)
            self.after(2000, self.destroy)

    # phase 1 : l’ET envoie N_CONNECT.req
    def _etablissement(self):
        self._log("=== Phase d'établissement de connexion ===")
        # choix stations aléatoires identiques au backend
        src_station = self.reseau.pick_random_station(-1)
        dst_station = self.reseau.pick_random_station(src_station.adresse)
        self.src = src_station.adresse
        self.dst = dst_station.adresse
        secteur = f"src {self.src} → dst {self.dst}"
        self._log(f"Demande de connexion {secteur}")
        self._animate_arrow("AtoB")
        self._bubble("N_CONNECT.req", "AtoB")
        # on formule la demande via backend
        from NConnect import NConnect
        paquet_req = NConnect.demande_connexion(1, self.src, self.dst)
        # stocker la réponse (PaquetCommunicationEtablie ou autre)
        self.rep_er = self.ER.demande_de_connexion(paquet_req)
    # phase 2 : l’utilisateur accepte ou refuse la connexion
    def _choix_connexion(self):
        if self.rep_er is None:
            # Timeout : pas de réponse du distant
            self._log("Pas de réponse du distant (timeout)")
            with open(S_ECR, "w", encoding="utf-8") as f:
                f.write("KO 1 – timeout\n")
            retry = messagebox.askyesno("Nouvelle tentative", "Voulez-vous réessayer ?")
            if retry:
                self.phase = 0
                self.btn_next.config(text="Démarrer la simulation", state=tk.NORMAL)
                self.txt.config(state=tk.NORMAL)
                self.txt.delete("1.0", tk.END)
                self.txt.config(state=tk.DISABLED)
                self._draw_network()
            else:
                self._log("Simulation interrompue par l'utilisateur")
                self.after(2000, self.destroy)
            return

        if self.rep_er.type == "00001111":
            # Connexion acceptée
            self._animate_arrow("BtoA")
            self._bubble("N_CONNECT.resp", "BtoA")
            self._log("[N_CONNECT.resp] Réponse de B (acceptée)")
            self._animate_arrow("BtoA")
            self._bubble("N_CONNECT.conf", "BtoA")
            self._log("[N_CONNECT.conf] Connexion confirmée à A")
            self.no_connexion_actuelle = int(self.rep_er.no_connexion, 2)
            return

        # Cas de refus (PaquetIndicationLiberation)
        self._animate_arrow("BtoA")
        self._bubble("N_DISCONNECT.req", "BtoA")

        # Différencier selon la raison
        if hasattr(self.rep_er, 'raison'):
            if self.rep_er.raison == "00000010":
                self._log("[N_DISCONNECT.req] Refus de la connexion par le fournisseur")
                refus_message = "KO 1 – refus fournisseur"
            elif self.rep_er.raison == "00000001":
                self._log("[N_DISCONNECT.req] Refus de la connexion par B")
                refus_message = "KO 1 – refus destinataire"
            else:
                self._log("[N_DISCONNECT.req] Refus de la connexion (raison inconnue)")
                refus_message = "KO 1 – refus inconnu"
        else:
            self._log("[N_DISCONNECT.req] Refus de la connexion (raison absente)")
            refus_message = "KO 1 – refus inconnu"

        self._log("[N_DISCONNECT.ind] Notification à A")
        self._log("Connexion refusée")

        # Écriture du résultat KO dans S_ecr.txt
        with open(S_ECR, "w", encoding="utf-8") as f:
            f.write(f"{refus_message}\n")

        retry = messagebox.askyesno("Nouvelle tentative", "Voulez-vous réessayer ?")
        if retry:
            self.phase = 0
            self.btn_next.config(text="Démarrer la simulation", state=tk.NORMAL)
            self.txt.config(state=tk.NORMAL)
            self.txt.delete("1.0", tk.END)
            self.txt.config(state=tk.DISABLED)
            self._draw_network()
        else:
            self._log("Simulation interrompue par l'utilisateur")
            self.after(2000, self.destroy)

    def _handle_refus(self, message):
        # Écriture dans S_ecr.txt
        with open(S_ECR, "w", encoding="utf-8") as f:
            f.write(f"{message}\n")

        retry = messagebox.askyesno("Nouvelle tentative", "Voulez-vous réessayer ?")
        if retry:
            self._reset_gui()
            self.phase = 0
            self.btn_next.config(text="Démarrer la simulation", state=tk.NORMAL)
        else:
            self._log("Simulation interrompue par l'utilisateur")
            self.btn_next.config(state=tk.DISABLED)  # 🔥 désactiver bouton
            self.entry.config(state=tk.DISABLED)
            self.btn_send.config(state=tk.DISABLED)
            self.after(2000, self.destroy)

    # phase 3 : transfert d’un message tapé par l’utilisateur
    def _transfert(self):
        self.entry.config(state=tk.NORMAL)
        self.btn_send.config(state=tk.NORMAL)
        self._log("=== Phase de transfert de données - écrivez un message et cliquez sur Envoyer ===")

    # après clic « Envoyer »
    def _send_data(self):
        # Si on n'a pas de connexion réseau active, on ignore l'envoi
        if self.no_connexion_actuelle is None:
            return
        msg = self.entry.get()
        if not msg:
            return
        self.entry.delete(0, tk.END)
        # backend – segmentation + écriture fichiers
        self.ER.envoyer_message(self.no_connexion_actuelle, msg)
        # visual
        self._animate_arrow("AtoB")
        self._bubble("DATA", "AtoB")
        self._log(f"A → B : '{msg}' (N_DATA.req)")
        # simu aléatoire ACK / NACK
        result = random.choice(["ACK", "NACK"])
        self._animate_arrow("BtoA")
        self._bubble(result, "BtoA")
        self._log(result)
        # Proposition d'envoyer un autre message
        another = messagebox.askyesno(
            "Envoyer un autre message",
            "Voulez‑vous envoyer un autre message sur cette connexion ?"
        )
        if another:
            self._log("Préparez votre prochain message…")
            # on garde entry ouvert pour un nouvel envoi
        else:
            # Désactiver l’envoi et passer en « prêt à libérer »
            self.entry.config(state=tk.DISABLED)
            self.btn_send.config(state=tk.DISABLED)
            # On ne déclenche pas tout de suite la libération :
            # on laisse l’utilisateur cliquer sur « Libérer connexion »
            self.phase = 3
            self.btn_next.config(text="Libérer connexion", state=tk.NORMAL)

    # phase 4 : libération
    def _liberation(self):
        self._log("=== Phase de libération ===")
        self._animate_arrow("AtoB")
        self._bubble("N_DISCONNECT.req", "AtoB")
        self.ER.liberer(self.no_connexion_actuelle)
        self._log("Connexion libérée")
        self._animate_arrow("BtoA")
        self._bubble("N_DISCONNECT.ind", "BtoA")

        # 🔵 Écriture OK dans S_ecr.txt
        with open(S_ECR, "w", encoding="utf-8") as f:
            f.write("OK 1 terminé\n")

        self.btn_send.config(state=tk.DISABLED)
        self.entry.config(state=tk.DISABLED)

if __name__ == "__main__":
    # création dossier Files si besoin
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    if not S_LEC.exists():
        GF.ecrire_fichier(str(S_LEC), "HELLO\nWORLD")
    app = ReseauSimGUI()
    app.mainloop()