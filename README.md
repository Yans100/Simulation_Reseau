
# Simulation réseau connecté — INF1005

Simulation Python du modèle OSI (couches transport et réseau) avec interface graphique Tkinter, animant les phases d'établissement, transfert et libération d'une connexion en mode connecté.

## Fonctionnalités

- Simulation des 3 phases d'une connexion en mode connecté : établissement, transfert, libération
- Couche réseau : demande de connexion, refus par fournisseur / destinataire, timeout, acceptation
- Couche transport : lecture de messages depuis fichier, orchestration des échanges N_CONNECT / N_DATA / N_DISCONNECT
- Segmentation automatique des messages > 128 octets en paquets
- Simulation d'acquittements ACK/NACK avec 80% de probabilité de succès
- Interface graphique Tkinter avec animation des échanges entre stations A et B
- Journalisation des échanges dans des fichiers texte (L_ecr, L_lec, S_ecr)

## Concepts démontrés

- Modèle OSI — couches transport et réseau
- Mode connecté (inspiré de X.25) : N_CONNECT, N_DATA, N_DISCONNECT
- Segmentation de paquets (max 128 octets)
- POO Python avec propriétés, enum, typage statique

## Technologies

- Python
- Tkinter (GUI)
- Librairie standard uniquement (aucune dépendance externe)

## Prérequis

Aucune dépendance externe — Python 3.10+ requis.

## Lancer le projet

```bash
# Interface graphique
python Main.py

# Mode console (batch)
python -c "from Main import main_console; main_console()"
```

Le dossier `Files/` est créé automatiquement au premier lancement.

## Structure

```
Main.py            — point d'entrée (GUI ou console)
SimGUI.py          — interface graphique Tkinter
CoucheTransport.py — couche transport (orchestration)
CoucheReseau.py    — couche réseau (connexion, paquets)
Reseau.py          — gestion des 255 stations
Station.py         — modèle d'une station réseau
Connexion.py       — modèle d'une connexion
EtatConnexion.py   — enum des états de connexion
NConnect.py        — primitives N_CONNECT
NDisconnect.py     — primitives N_DISCONNECT
NData.py           — primitives N_DATA
GestionFichiers.py — lecture/écriture des fichiers journaux
Files/             — fichiers de journalisation (S_lec, S_ecr, L_ecr, L_lec)
```

---

Projet universitaire solo — cours INF1005, UQTR.
