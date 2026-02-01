import pygame
import json


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur_base, couleur_survol):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur_base = couleur_base
        self.couleur_survol = couleur_survol
        self.font = pygame.font.Font(None, 40)

    def dessiner(self, surface):
        pos_souris = pygame.mouse.get_pos()
        # Changement de couleur si la souris est dessus
        if self.rect.collidepoint(pos_souris):
            couleur = self.couleur_survol
        else:
            couleur = self.couleur_base

        pygame.draw.rect(surface, couleur, self.rect, border_radius=12)
        pygame.draw.rect(
            surface, (255, 255, 255), self.rect, 3, border_radius=12
        )  # Bordure

        # Texte centré
        surface_texte = self.font.render(self.texte, True, (255, 255, 255))
        rect_texte = surface_texte.get_rect(center=self.rect.center)
        surface.blit(surface_texte, rect_texte)

    def est_clique(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if self.rect.collidepoint(event.pos):
                    return True
        return False


def dessiner_regles(screen):
    screen.fill((50, 50, 50))  # Fond gris foncé
    largeur = screen.get_width()
    hauteur = screen.get_height()
    milieu_x = largeur // 2

    font_titre = pygame.font.Font(None, 60)
    font_desc = pygame.font.Font(None, 30)

    # Titre
    titre = font_titre.render("COMMENT JOUER ?", True, (255, 215, 0))
    screen.blit(titre, (largeur // 2 - titre.get_width() // 2, 30))

    # --- ZONE GAUCHE : CLAVIER ---
    pygame.draw.rect(screen, (100, 100, 200), (50, 100, milieu_x - 100, 400), 2)
    titre_j1 = font_desc.render("JOUEUR 1 (Clavier)", True, (200, 200, 255))
    screen.blit(titre_j1, (milieu_x // 2 - titre_j1.get_width() // 2, 110))

    # Dessin des touches ZSDE
    # Centre de la zone gauche
    cx, cy = 50 + (milieu_x - 100) // 2, 100 + 200
    taille_touche = 60

    # Coordonnées relatives
    touches = [
        ("Z", cx - taille_touche, cy - taille_touche),  # Haut Gauche
        ("E", cx + taille_touche, cy - taille_touche),  # Haut Droite
        ("S", cx - taille_touche, cy + taille_touche),  # Bas Gauche
        ("D", cx + taille_touche, cy + taille_touche),  # Bas Droite
    ]

    for lettre, tx, ty in touches:
        pygame.draw.rect(
            screen, (255, 255, 255), (tx - 25, ty - 25, 50, 50), border_radius=5
        )
        txt = font_desc.render(lettre, True, (0, 0, 0))
        screen.blit(txt, (tx - txt.get_width() // 2, ty - txt.get_height() // 2))

    expl_j1 = font_desc.render(
        "Utilisez Z, S, D, E pour couper dans les zones", True, (200, 200, 200)
    )
    screen.blit(expl_j1, (milieu_x // 2 - expl_j1.get_width() // 2, 520))

    # --- ZONE DROITE : SOURIS ---
    pygame.draw.rect(
        screen, (200, 100, 100), (milieu_x + 50, 100, milieu_x - 100, 400), 2
    )
    titre_j2 = font_desc.render("JOUEUR 2 / SOLO (Souris)", True, (255, 200, 200))
    screen.blit(titre_j2, (milieu_x + milieu_x // 2 - titre_j2.get_width() // 2, 110))

    # Dessin symbolique souris
    pygame.draw.ellipse(
        screen, (255, 255, 255), (milieu_x + milieu_x // 2 - 30, 250, 60, 90), 3
    )
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (milieu_x + milieu_x // 2, 250),
        (milieu_x + milieu_x // 2, 280),
        3,
    )

    expl_j2 = font_desc.render(
        "Maintenez le clic gauche et glissez pour couper", True, (200, 200, 200)
    )
    screen.blit(expl_j2, (milieu_x + milieu_x // 2 - expl_j2.get_width() // 2, 520))


def dessiner_scores(screen):
    """
    Affiche l'historique des parties en 2 colonnes (1J et 2J).
    """
    from scores import (
        charger_scores,
        obtenir_statistiques,
        obtenir_historique_trie_par_score,
    )

    # Fond
    screen.fill((45, 45, 60))

    largeur = screen.get_width()
    hauteur = screen.get_height()
    milieu_x = largeur // 2

    # Polices
    font_titre = pygame.font.Font(None, 50)
    font_sous_titre = pygame.font.Font(None, 35)
    font_score = pygame.font.Font(None, 28)
    font_stats = pygame.font.Font(None, 24)

    # ========================================================================
    # TITRE PRINCIPAL
    # ========================================================================
    titre = font_titre.render("HISTORIQUE DES PARTIES", True, (255, 215, 0))
    screen.blit(titre, (largeur // 2 - titre.get_width() // 2, 15))

    # Ligne de séparation
    pygame.draw.line(screen, (100, 100, 100), (20, 55), (largeur - 20, 55), 2)

    # ========================================================================
    # COLONNE GAUCHE : MODE 1 JOUEUR
    # ========================================================================
    col1_x = 30
    col1_largeur = milieu_x - 50

    # Titre colonne
    titre_1j = font_sous_titre.render("MODE 1 JOUEUR", True, (100, 200, 100))
    screen.blit(titre_1j, (col1_x + col1_largeur // 2 - titre_1j.get_width() // 2, 70))

    # Stats
    stats_1j = obtenir_statistiques("1j")
    y_stats = 105
    if stats_1j:
        txt_stats = font_stats.render(
            f"Parties: {stats_1j['nombre_parties']} | Record: {stats_1j['meilleur_score']} | Moy: {stats_1j['score_moyen']}",
            True,
            (150, 150, 150),
        )
        screen.blit(txt_stats, (col1_x, y_stats))

    # En-têtes
    y_entete = 135
    pygame.draw.line(
        screen,
        (80, 80, 80),
        (col1_x, y_entete + 25),
        (col1_x + col1_largeur, y_entete + 25),
        1,
    )

    screen.blit(font_stats.render("#", True, (180, 180, 180)), (col1_x, y_entete))
    screen.blit(
        font_stats.render("SCORE", True, (180, 180, 180)), (col1_x + 40, y_entete)
    )
    screen.blit(
        font_stats.render("NIV", True, (180, 180, 180)), (col1_x + 120, y_entete)
    )
    screen.blit(
        font_stats.render("DATE", True, (180, 180, 180)), (col1_x + 180, y_entete)
    )

    # Liste des scores 1J
    historique_1j = obtenir_historique_trie_par_score("1j")
    y_score = y_entete + 35
    max_lignes = (hauteur - y_score - 60) // 28

    for i, partie in enumerate(historique_1j[:max_lignes]):
        y = y_score + i * 28

        # Couleur selon rang
        if i == 0:
            couleur = (255, 215, 0)
        elif i == 1:
            couleur = (192, 192, 192)
        elif i == 2:
            couleur = (205, 127, 50)
        else:
            couleur = (220, 220, 220)

        screen.blit(font_score.render(f"{i+1}.", True, couleur), (col1_x, y))
        screen.blit(
            font_score.render(str(partie.get("score", 0)), True, couleur),
            (col1_x + 40, y),
        )
        screen.blit(
            font_score.render(str(partie.get("niveau", 1)), True, couleur),
            (col1_x + 120, y),
        )

        date_str = partie.get("date", "")
        if date_str:
            try:
                from datetime import datetime

                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                date_affichee = dt.strftime("%d/%m %H:%M")
            except:
                date_affichee = date_str[:10]
        else:
            date_affichee = "-"
        screen.blit(font_score.render(date_affichee, True, couleur), (col1_x + 180, y))

    # ========================================================================
    # LIGNE DE SÉPARATION VERTICALE
    # ========================================================================
    pygame.draw.line(
        screen, (100, 100, 100), (milieu_x, 65), (milieu_x, hauteur - 50), 2
    )

    # ========================================================================
    # COLONNE DROITE : MODE 2 JOUEURS
    # ========================================================================
    col2_x = milieu_x + 20
    col2_largeur = largeur - milieu_x - 50

    # Titre colonne
    titre_2j = font_sous_titre.render("MODE 2 JOUEURS", True, (100, 150, 255))
    screen.blit(titre_2j, (col2_x + col2_largeur // 2 - titre_2j.get_width() // 2, 70))

    # Stats
    stats_2j = obtenir_statistiques("2j")
    if stats_2j:
        txt_stats_2j = font_stats.render(
            f"Parties: {stats_2j['nombre_parties']} | J1: {stats_2j.get('victoires_j1', 0)} | J2: {stats_2j.get('victoires_j2', 0)}",
            True,
            (150, 150, 150),
        )
        screen.blit(txt_stats_2j, (col2_x, y_stats))

    # En-têtes
    pygame.draw.line(
        screen,
        (80, 80, 80),
        (col2_x, y_entete + 25),
        (col2_x + col2_largeur, y_entete + 25),
        1,
    )

    screen.blit(font_stats.render("#", True, (180, 180, 180)), (col2_x, y_entete))
    screen.blit(
        font_stats.render("GAGNANT", True, (180, 180, 180)), (col2_x + 40, y_entete)
    )
    screen.blit(
        font_stats.render("DATE", True, (180, 180, 180)), (col2_x + 150, y_entete)
    )

    # Liste des parties 2J
    historique_2j = charger_scores("2j")

    for i, partie in enumerate(historique_2j[:max_lignes]):
        y = y_score + i * 28

        gagnant = partie.get("gagnant", "?")
        if gagnant == "J1":
            couleur = (100, 200, 100)
            txt_gagnant = "Joueur 1"
        elif gagnant == "J2":
            couleur = (100, 150, 255)
            txt_gagnant = "Joueur 2"
        else:
            couleur = (255, 165, 0)
            txt_gagnant = "Egalite"

        screen.blit(font_score.render(f"{i+1}.", True, (220, 220, 220)), (col2_x, y))
        screen.blit(font_score.render(txt_gagnant, True, couleur), (col2_x + 40, y))

        date_str = partie.get("date", "")
        if date_str:
            try:
                from datetime import datetime

                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                date_affichee = dt.strftime("%d/%m %H:%M")
            except:
                date_affichee = date_str[:10]
        else:
            date_affichee = "-"
        screen.blit(
            font_score.render(date_affichee, True, (220, 220, 220)), (col2_x + 150, y)
        )

    # ========================================================================
    # INSTRUCTION EN BAS
    # ========================================================================
    txt_instruction = pygame.font.Font(None, 22).render(
        "Appuyez sur R pour effacer l'historique", True, (100, 100, 100)
    )
    screen.blit(
        txt_instruction, (largeur // 2 - txt_instruction.get_width() // 2, hauteur - 35)
    )
