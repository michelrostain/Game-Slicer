import pygame
import math
from objets import Glacon, Bombe

# Variables pour le slicing à la souris
slicing = False
# Liste des positions de la souris pendant le tranchage (pour dessiner la traînée)
slice_points = []

# ============================================================================
# VARIABLES POUR LE SYSTÈME DE COMBO
# ============================================================================
# Un combo, c'est quand le joueur tranche plusieurs fruits en un seul geste
# (sans relâcher le bouton de la souris)
#
# RÈGLES DU COMBO :
# - 1 fruit tranché = +1 point (pas de bonus)
# - 2 fruits tranchés d'un coup = +2 points (pas de bonus)
# - 3 fruits tranchés d'un coup = +2 points de BONUS (+1 bonus)
# - 4 fruits tranchés d'un coup = +3 points de BONUS (+2 bonus)
# - etc. : bonus = nombre_fruits - 2 (si >= 3 fruits)
#
# FORMULE : points = fruits_tranches + max(0, fruits_tranches - 2)
# ============================================================================

# Compteur de fruits tranchés pendant le geste actuel
combo_actuel = 0


def start_slice(mouse_pos):
    """
    :Param: Démarre le slicing quand le joueur appuie sur le bouton de la souris.
    Args:
        mouse_pos (tuple): Position initiale de la souris (x, y)
    """
    global slicing, slice_points, combo_actuel

    # Active le mode tranchage
    slicing = True

    # Commence une nouvelle traînée avec la position actuelle
    slice_points = [mouse_pos]

    # Réinitialise le combo (nouveau geste = nouveau combo)
    combo_actuel = 0


def update_slice(mouse_pos, mes_fruits, screen_width, nombre_de_joueurs=1):
    """
    :Param: Met à jour la traînée ET vérifie les collisions en temps réel (sous le curseur)

    Args:
        mouse_pos (tuple): Position actuelle de la souris (x, y)
        mes_fruits (list): Liste des fruits actuellement à l'écran
        screen_width (int): Largeur de l'écran (pour gérer les 2 joueurs)
        nombre_de_joueurs (int): Nombre de joueurs (1 ou 2)

    Retourne:
        str: "freeze" si un glaçon a été tranché
        str: "game_over" si une bombe a été tranchée
        int: 1 si un fruit normal a été tranché
        None: si rien n'a été tranché
    """
    global slice_points, combo_actuel

    # Si on n'est pas en mode slicing, on ne fait rien
    if not slicing:
        return None

    # ========================================================================
    # ÉTAPE 1 : Mise à jour de la traînée visuelle
    # ========================================================================

    # Ajoute la position actuelle de la souris à la traînée
    slice_points.append(mouse_pos)

    # Limite la longueur de la traînée à 15 points pour éviter une traînée infinie
    if len(slice_points) > 15:
        slice_points.pop(0)

    # ========================================================================
    # ÉTAPE 2 : VÉRIFICATION DES COLLISIONS (POINT vs CERCLE)
    # ========================================================================

    # Position de la souris
    mx, my = mouse_pos

    # Milieu de l'écran (pour 2 joueurs)
    milieu_x = screen_width // 2

    # On parcourt une copie de la liste [:] pour pouvoir supprimer dedans sans bug
    for fruit in mes_fruits[:]:

        # --- VÉRIFICATION DE LA ZONE (J2 ne peut couper qu'à droite) ---
        if nombre_de_joueurs == 2:
            # Si le fruit est à GAUCHE, le joueur 2 (Souris) ne peut pas le toucher
            if fruit.x < milieu_x:
                continue
            # Protection supplémentaire : Si la SOURIS est à gauche, on ne coupe pas
            if mx < milieu_x:
                continue

        # --- VÉRIFICATION COLLISION (POINT vs CERCLE) ---
        # On regarde simplement si le curseur de la souris est DANS le rayon du fruit
        # On utilise la formule de distance euclidienne :
        # distance = √((x2-x1)² + (y2-y1)²)
        #
        # Si cette distance est inférieure au rayon du fruit,
        # alors la souris est "dans" le fruit = collision !
        distance = math.sqrt((mx - fruit.x) ** 2 + (my - fruit.y) ** 2)

        #  --- COLLISION DÉTECTÉE ---
        if distance < fruit.radius:
            # Vérifie qu'on ne coupe pas un fruit déjà coupé
            if not fruit.sliced:

                # ============================================================
                # CAS 1 : C'est un GLAÇON
                # ============================================================
                if isinstance(fruit, Glacon) or fruit.type == "ice":
                    mes_fruits.remove(fruit)

                    # Détermine quel joueur a tranché (basé sur la position de la souris)
                    if nombre_de_joueurs == 2:
                        if mx >= milieu_x:
                            print("Glacon tranche par J2 !")
                            return "freeze_j2"
                        else:
                            print("Glacon tranche par J1 !")
                            return "freeze_j1"
                    else:
                        print("Glacon tranche !")
                        return "freeze"

                # ============================================================
                # CAS 2 : C'est une BOMBE
                # ============================================================
                if isinstance(fruit, Bombe) or fruit.type == "bombe":
                    mes_fruits.remove(fruit)  # La bombe disparaît
                    print("BOOM ! Bombe tranchée !")
                    return "game_over"

                # ============================================================
                # CAS 3 : C'est un FRUIT (normal)
                # ============================================================

                # Incrémente le compteur de combo
                combo_actuel += 1

                # Si le fruit a des états (images différentes selon l'état)
                if fruit.images_set:
                    fruit.couper()  # Change l'image vers "cut"
                    # Le fruit reste à l'écran et continue de tomber
                else:
                    # Fruit simple : on le supprime directement
                    mes_fruits.remove(fruit)

                print(f"🍎 Fruit tranché ! Combo actuel : {combo_actuel}")

                # Retourne 1 pour signaler qu'un fruit a été tranché
                # (le calcul du score avec bonus se fait dans end_slice)
                return 1

    # Aucune collision détectée
    return None


def end_slice(mes_fruits, screen_width=None, nombre_de_joueurs=1):
    """
    :Param: Termine le slicing quand le joueur relâche le bouton de la souris et calcule le score du combo.

    Args:
        mes_fruits (list): Liste des fruits actuellement à l'écran
        screen_width (int): Largeur de l'écran (pour gérer les 2 joueurs)
        nombre_de_joueurs (int): Nombre de joueurs (1 ou 2)

    Retourne:
        int: le score total à ajouter (fruits tranchés + bonus combo). Retourne 0 si aucun fruit tranché.
    """
    global slicing, slice_points, combo_actuel

    # Désactive le mode tranchage
    slicing = False

    # Réinitialise la traînée visuelle
    slice_points = []

    # Calcul du score basé sur le combo
    if combo_actuel == 0:
        # Aucun fruit tranché pendant ce geste
        return 0

    # Calcul du bonus
    # max(0, x) retourne 0 si x est négatif, sinon retourne x
    # Cela évite d'avoir un bonus négatif pour 1 ou 2 fruits
    bonus = max(0, combo_actuel - 2)

    # Score total = fruits tranchés + bonus
    score_geste = combo_actuel + bonus

    # Affiche le résultat du combo
    if bonus > 0:
        print(
            f"COMBO x{combo_actuel} ! {combo_actuel} fruits + {bonus} bonus = {score_geste} points !"
        )
    elif combo_actuel > 0:
        print(f"✓ {combo_actuel} fruit(s) tranché(s) = {score_geste} point(s)")

    # Réinitialise le compteur pour le prochain geste
    fruits_tranches = combo_actuel  # Sauvegarde pour le retour
    combo_actuel = 0

    return score_geste


def handle_keyboard_inputs(
    mes_fruits, screen_width, screen_height, key, nombre_de_joueurs=1
):
    """
    :Param: Gère les entrées clavier pour le joueur 1 (ZSDE) en mode 2 joueurs.

    TOUCHES UTILISÉES (Joueur 1 - Zone gauche de l'écran) :
    - Z : Tranche les fruits dans le quart HAUT-GAUCHE
    - E : Tranche les fruits dans le quart HAUT-DROIT (de la zone J1)
    - S : Tranche les fruits dans le quart BAS-GAUCHE
    - D : Tranche les fruits dans le quart BAS-DROIT (de la zone J1)

    SCHÉMA DE LA ZONE JOUEUR 1 :
    +-------+-------+
    |   Z   |   E   |
    +-------+-------+
    |   S   |   D   |
    +-------+-------+

    Args:
        mes_fruits (list): Liste des fruits actuellement à l'écran
        screen_width (int): Largeur de l'écran
        screen_height (int): Hauteur de l'écran
        key (int): Touche appuyée (pygame.K_*)
        nombre_de_joueurs (int): Nombre de joueurs (1 ou 2)

    Retourne:
        str: "freeze" si un glaçon a été tranché
        str: "game_over" si une bombe a été tranchée
        None: si rien n'a été tranché
        int : le score total à ajouter (fruits tranchés + bonus combo). Retourne 0 si aucun fruit tranché.
    """

    # Calcul du milieu de l'écran
    milieu_x = screen_width // 2

    # Variable pour indiquer si un bonus a été activé
    bonus_active = None

    # Définition des 4 zones du joueur 1 (Gauche)
    # Format: (x_min, y_min, x_max, y_max)
    zones = {
        pygame.K_z: (0, 0, milieu_x // 2, screen_height // 2),  # Haut-gauche
        pygame.K_s: (0, screen_height // 2, milieu_x // 2, screen_height),  # Bas-gauche
        pygame.K_d: (
            milieu_x // 2,
            screen_height // 2,
            milieu_x,
            screen_height,
        ),  # Bas-droite (de la zone J1)
        pygame.K_e: (
            milieu_x // 2,
            0,
            milieu_x,
            screen_height // 2,
        ),  # Haut-droite (de la zone J1)
    }

    # Vérifie si la touche pressée correspond à une zone
    if key not in zones:
        return None  # Touche non reconnue

    # Récupère les limites de la zone correspondante
    zone = zones[key]
    x_min, y_min, x_max, y_max = zone

    # Compteur de fruits tranchés pour le combo clavier
    fruits_tranches = 0

    # Parcours des fruits dans la zone définie
    for fruit in mes_fruits[:]:
        # Vérifie si le fruit est dans la zone
        if x_min <= fruit.x <= x_max and y_min <= fruit.y <= y_max:

            # ================================================================
            # CAS BOMBE
            # ================================================================
            if isinstance(fruit, Bombe) or fruit.type == "bombe":
                mes_fruits.remove(fruit)
                print("[J1 CLAVIER] Bombe tranchée ! GAME OVER !")
                bonus_active = "game_over"
                # On continue quand même pour trancher les autres fruits
                # (mais le jeu va s'arrêter après)

            # ================================================================
            # CAS GLAÇON
            # ================================================================
            elif isinstance(fruit, Glacon) or fruit.type == "ice":
                mes_fruits.remove(fruit)
                # En mode 2 joueurs, le clavier = Joueur 1
                if nombre_de_joueurs == 2:
                    print("[J1 CLAVIER] Glaçon tranché ! Freeze J1 !")
                    bonus_active = "freeze_j1"
                else:
                    print("[J1 CLAVIER] Glaçon tranché ! Temps gelé !")
                    bonus_active = "freeze"

            # ================================================================
            # CAS FRUIT NORMAL
            # ================================================================
            elif not fruit.sliced:  # Vérifie qu'il n'est pas déjà tranché

                # Si le fruit a des états visuels (comme la poire)
                if fruit.images_set:
                    fruit.couper()  # Change l'image vers "cut"
                else:
                    mes_fruits.remove(fruit)  # Supprime le fruit simple

                fruits_tranches += 1

    # ========================================================================
    # CALCUL DU SCORE AVEC BONUS COMBO (même formule que pour la souris)
    # ========================================================================

    if fruits_tranches > 0:
        bonus = max(0, fruits_tranches - 2)
        score_total = fruits_tranches + bonus

        if bonus > 0:
            print(
                f"[J1 CLAVIER] COMBO x{fruits_tranches} ! +{bonus} bonus = {score_total} points !"
            )
        else:
            print(f"[J1 CLAVIER] {fruits_tranches} fruit(s) = {score_total} point(s)")

        # Si un effet spécial a été déclenché, on le retourne en priorité
        if bonus_active:
            return bonus_active

        return score_total

    # Retourne l'effet spécial s'il y en a un, sinon None
    return bonus_active


def draw_slice(screen):
    """
    :Param: Dessine la traînée visuelle
    Args:
        screen (pygame.Surface): Surface de l'écran où dessiner
    """

    # On ne dessine que si on est en mode slicing et qu'il y a assez de points
    if slicing and len(slice_points) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, slice_points, 3)


# ============================================================================
# FONCTION : get_combo_actuel (utilitaire)
# ============================================================================
def get_combo_actuel():
    """
    :Param: Retourne le nombre de fruits tranchés dans le combo en cours.

    UTILITÉ :
    - Permet d'afficher le combo en temps réel à l'écran
    - Peut être utilisé pour des effets visuels (ex: texte "COMBO x3!")

    Retourne:
        int: Nombre de fruits tranchés dans le geste actuel
    """
    return combo_actuel
