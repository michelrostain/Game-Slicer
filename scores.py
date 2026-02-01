# ============================================================================
# FICHIER : scores.py
# DESCRIPTION : Gestion des scores (sauvegarde, chargement, réinitialisation)
# ============================================================================
#
# CE FICHIER GÈRE :
# - La création automatique du fichier JSON de scores
# - Le chargement des scores existants
# - La réinitialisation des scores
#
# ============================================================================

import json
import os
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

# Nom du fichier où seront sauvegardés les scores
# Il sera créé automatiquement dans le même dossier que le jeu
FICHIER_SCORES = "scores.json"


# ============================================================================
# On crée le fichier scores.json s'il n'existe pas
# ============================================================================
def creer_fichier_scores_si_absent():
    """
    La fonction `creer_fichier_scores_si_absent` crée un fichier avec des données initiales s'il n'existe pas déjà.
    :return: La fontion `creer_fichier_scores_si_absent()` retourne une valeur booléenne. Elle retourne `True` si le fichier a été créé avec succès, et `False` sinon.
    """

    # Vérifie si le fichier existe déjà sur le disque
    if not os.path.exists(FICHIER_SCORES):
        # Le fichier n'existe pas, on va le créer

        # Structure initiale : un dictionnaire avec une liste vide
        donnees_initiales = {
            "historique_1j": [],  # Parties en mode 1 joueur
            "historique_2j": [],  # Parties en mode 2 joueurs
        }

        # Ouvre le fichier en mode écriture ('w' = write = écriture)
        # encoding="utf-8" permet de gérer les caractères spéciaux (accents, émojis)
        # Le bloc "with" ferme automatiquement le fichier à la fin
        with open(FICHIER_SCORES, "w", encoding="utf-8") as fichier:
            # json.dump() convertit le dictionnaire Python en texte JSON
            # et l'écrit dans le fichier
            # indent=4 : ajoute des espaces pour rendre le fichier lisible
            # ensure_ascii=False : permet les caractères non-ASCII (accents)
            json.dump(donnees_initiales, fichier, indent=4, ensure_ascii=False)

        print(f"✅ Fichier {FICHIER_SCORES} créé avec succès !")
        return True  # Le fichier a été créé

    # Le fichier existait déjà, on ne fait rien
    return False


# ============================================================================
# FONCTION : charger_scores
# ============================================================================
def charger_scores(mode="1j"):
    """
    :Param: Charge les scores depuis le fichier JSON.

    :return: liste des scores sinon une liste vide en cas d'erreur ou si aucun score n'existe.

    Exemple: [{"nom": "AAA", "score": 100, "niveau": 5}, ...]
    """
    # Étape 1 : S'assurer que le fichier existe
    creer_fichier_scores_si_absent()

    try:
        # Étape 2 : Ouvrir le fichier en mode lecture ('r' = read = lecture)
        with open(FICHIER_SCORES, "r", encoding="utf-8") as fichier:
            # Étape 3 : json.load() lit le JSON et le convertit en dictionnaire Python
            donnees = json.load(fichier)

            # Comptatibilité avec l'ancien format (avant v1.2.0) qui n'avait qu'un seul historique
            if "historique" in donnees and "historique_1j" not in donnees:
                donnees = {
                    "historique_1j": donnees.get("historique", []),
                    "historique_2j": [],
                }
                # On sauvegarde immédiatement dans le nouveau format
                with open(FICHIER_SCORES, "w", encoding="utf-8") as f:
                    json.dump(donnees, f, indent=4, ensure_ascii=False)

            cle = f"historique_{mode}"
            historique = donnees.get(cle, [])

            # On trie l'historique par score décroissant, on utilise la clé "date" qui est au format ISO, donc triable directement
            historique.sort(key=lambda x: x.get("date", ""), reverse=True)

            # On retourne l'historique
            return historique

    except (json.JSONDecodeError, FileNotFoundError):
        # Le fichier est corrompu ou illisible
        print(
            f"⚠️ Erreur de lecture du fichier {FICHIER_SCORES}, réinitialisation en cours..."
        )

        # On recrée un fichier propre
        reinitialiser_scores()
        return []  # Retourne une liste vide


# ============================================================================
# FONCTION : sauvegarder_score
# ============================================================================
def sauvegarder_score(score, niveau, duree_secondes=0, mode="1j", gagnant=None):
    """
    :Param: Sauvegarde une nouvelle partie dans l'historique.

    Args:
        score (int): Le score obtenu (nombre de fruits tranchés avec bonus combo)
        niveau (int): Le niveau atteint dans la partie
        duree_secondes (int): La durée de la partie en secondes (optionnel, par défaut 0)
        mode (str): Le mode de jeu ("1j" ou "2j")
        gagnant (str): Le joueur gagnant en mode 2 joueurs ("J1", "J2" ou "Égalité")

    :Return:
        L'index de la partie dans le classement trié par score (1 = meilleur)
            Utile pour afficher "Vous êtes Xème !"
    """

    # Charge tout l'historique
    creer_fichier_scores_si_absent

    try:
        with open(FICHIER_SCORES, "r", encoding="utf-8") as fichier:
            donnees = json.load(fichier)
    except:
        donnees = {"historique_1j": [], "historique_2j": []}

    # S'assure que les clés existent
    if "historique_1j" not in donnees:
        donnees["historique_1j"] = []
    if "historique_2j" not in donnees:
        donnees["historique_2j"] = []

    # Créer le nouveau score sous forme de dictionnaire
    # - .upper() : convertit en majuscules ("abc" -> "ABC")
    # - [:3] : garde seulement les 3 premiers caractères
    nouvelle_partie = {
        "score": score,
        "niveau": niveau,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # Date/heure actuelle au format "YYYY-MM-DD HH:MM:SS"
        "duree_secondes": duree_secondes,
    }

    # Ajoute le gagnant si en mode 2 joueurs
    if mode == "2j" and gagnant:
        nouvelle_partie["gagnant"] = gagnant

    # Ajoute la nouvelle partie à l'historique approprié
    cle = f"historique_{mode}"
    donnees[cle].append(nouvelle_partie)

    # Sauvegarde l'historique mis à jour dans le fichier
    with open(FICHIER_SCORES, "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, indent=4, ensure_ascii=False)

    # Calcule la position dans le classement (trié par score décroissant)
    # On trie temporairement pour trouver la position
    # lambda est une mini-fonction anonyme (sans nom)
    # lambda x: x["score"] équivaut à :
    #   def fonction_tri(x):
    #       return x["score"]
    historique_trie = sorted(donnees[cle], key=lambda x: x["score"], reverse=True)

    position = 1
    for i, partie in enumerate(historique_trie):
        if partie["score"] == score and partie["date"] == nouvelle_partie["date"]:
            position = i + 1
            break

    print(
        f"Partie {mode.upper()} enregistree ! Score: {score} | Position: {position}eme"
    )

    return position


# ============================================================================
# FONCTION : reinitialiser_scores
# ============================================================================
def reinitialiser_scores():
    """
    :Param: Efface tous les scores et recrée un fichier vide quand l'utilisateur appuie sur "R" dans l'écran des scores ou quand le fichier est corrompu.

    ATTENTION : Cette action est IRRÉVERSIBLE !
    Tous les scores seront perdus définitivement.

    :Return:
        bool: True si la réinitialisation a réussi, False sinon
    """
    try:
        # Crée un fichier avec une liste vide
        donnees = {"historique_1j": [], "historique_2j": []}

        with open(FICHIER_SCORES, "w", encoding="utf-8") as fichier:
            json.dump(donnees, fichier, indent=4, ensure_ascii=False)

        print("🗑️ Tous les scores ont été effacés !")
        return True

    except Exception as erreur:
        # Exception = n'importe quelle erreur
        print(f"❌ Erreur lors de la réinitialisation : {erreur}")
        return False


# ============================================================================
# FONCTION : obtenir_meilleur_score
# ============================================================================
def obtenir_meilleur_score(mode="1j"):
    """
    :Param: Retourne le meilleur score enregistré (le record).

    :Return:
        dict: Le meilleur score {"nom": "AAA", "score": 150, "niveau": 8}
        Retourne None si aucun score enregistré
    """
    historique = charger_scores(mode)

    # Si la liste n'est pas vide, le premier élément est le meilleur
    # (car la liste est triée du meilleur au moins bon)
    if not historique:
        return None

    # Trouve le score maximum
    return max(historique, key=lambda x: x["score"])


# ============================================================================
# FONCTION : est_nouveau_record
# ============================================================================
def est_nouveau_record(score, mode="1j"):
    """
    :Param: Vérifie si un score bat le record actuel.

    Args:
        score (int): Le score à vérifier

    :Return:
        bool: True si c'est un nouveau record, False sinon
    """
    meilleur = obtenir_meilleur_score(mode)

    # S'il n'y a aucun score, c'est forcément un record !
    if meilleur is None:
        return True

    # Compare le score avec le record actuel
    return score > meilleur["score"]


# ============================================================================
# FONCTION : obtenir_statistiques
# ============================================================================
def obtenir_statistiques(mode="1j"):
    """
    Calcule des statistiques sur l'historique des parties.

    :return: Dictionnaire avec les statistiques :
                {
                    "nombre_parties": int,
                    "meilleur_score": int,
                    "score_moyen": float,
                    "niveau_max": int,
                    "niveau_moyen": float
                }
            Retourne None si aucune partie jouée
    """
    historique = charger_scores(mode)

    if not historique:
        return None

    scores = [p["score"] for p in historique]
    niveaux = [p["niveau"] for p in historique]

    stats = {
        "nombre_parties": len(historique),
        "meilleur_score": max(scores),
        "score_moyen": round(sum(scores) / len(scores), 1),
        "niveau_max": max(niveaux),
        "niveau_moyen": round(sum(niveaux) / len(niveaux), 1),
    }

    # Stats spécifiques au mode 2 joueurs
    if mode == "2j":
        victoires_j1 = sum(1 for p in historique if p.get("gagnant") == "J1")
        victoires_j2 = sum(1 for p in historique if p.get("gagnant") == "J2")
        egalites = sum(1 for p in historique if p.get("gagnant") == "egalite")

        stats["victoires_j1"] = victoires_j1
        stats["victoires_j2"] = victoires_j2
        stats["egalites"] = egalites

    return stats


# ============================================================================
# FONCTION : obtenir_historique_trie_par_score
# ============================================================================
def obtenir_historique_trie_par_score(mode="1j"):
    """
    Retourne l'historique trié par score décroissant (meilleur en premier).

    :return: Liste des parties triées par score
    """
    historique = charger_scores(mode)
    return sorted(historique, key=lambda x: x["score"], reverse=True)


# ============================================================================
# FONCTIONS OBSOLÈTES (gardées pour compatibilité)
# ============================================================================
def est_dans_classement(score):
    """
    Fonction obsolète - Toutes les parties sont maintenant enregistrées.
    Retourne toujours True pour compatibilité.
    """
    return True
