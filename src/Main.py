"""
Point d'entrée de la simulation réseau‑transport.
"""

from pathlib import Path

# backend console
from Reseau import Reseau
from CoucheReseau import CoucheReseau
from CoucheTransport import CoucheTransport
from GestionFichiers import GestionFichiers as GF

# frontend graphique
from SimGUI import ReseauSimGUI

FILES_DIR = Path("Files")
S_LEC      = FILES_DIR / "S_lec.txt"
L_ECR      = FILES_DIR / "L_ecr.txt"
L_LEC      = FILES_DIR / "L_lec.txt"
S_ECR      = FILES_DIR / "S_ecr.txt"


def prepare_demo_input() -> None:
    """Crée Files/S_lec.txt avec 150 octets si le fichier n’existe pas."""
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    if not S_LEC.exists():
        GF.ecrire_fichier(str(S_LEC), "A" * 150)  # >128 octets pour tester la segmentation


def main_console() -> None:
    """Simulation en mode console/batch."""
    prepare_demo_input()
    reseau = Reseau()
    er     = CoucheReseau(reseau, str(L_ECR), str(L_LEC))
    et     = CoucheTransport(reseau, er, s_lec=str(S_LEC), s_ecr=str(S_ECR))
    et.run()
    print(
        "\nSimulation  terminée – consultez Files/S_ecr.txt, L_ecr.txt, L_lec.txt\n"
    )


def main() -> None:
    """Lance directement l'interface graphique."""
    prepare_demo_input()
    app = ReseauSimGUI()
    app.mainloop()


if __name__ == "__main__":
    main()