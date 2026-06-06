from typing import Optional

"""Classe pour gérer les opérations de lecture et d'écriture des fichiers."""
class GestionFichiers:
     
    @staticmethod
    def ecrire_fichier(path: str, message: str) -> None:
        """Ajouter un message à la fin du fichier (mode append)."""
        try:
            with open(path, "a") as file:           # ← passage en mode 'a'
                 # écrire le message et s'assurer d'un saut de ligne final
                 file.write(message.rstrip("\n") + "\n")
            print(f"Écriture dans {path} (append) réussie !")
        except IOError as e:
            print(f"Erreur lors de l'écriture (append) dans {path}: {e}")

    @staticmethod
    def lire_fichier(path: str) -> Optional[str]:
        """Lire le contenu d'un fichier."""
        try:
            with open(path, "r") as file:
                return file.read()
        except IOError as e:
            print(f"Erreur lors de la lecture de {path}: {e}")
            return None

    @staticmethod
    def lire_lignes(path: str) -> list[str]:
        contenu = GestionFichiers.lire_fichier(path)
        return contenu.splitlines() if contenu else []
