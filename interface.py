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
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=12) # Bordure
        
        # Texte centré
        surface_texte = self.font.render(self.texte, True, (255, 255, 255))
        rect_texte = surface_texte.get_rect(center=self.rect.center)
        surface.blit(surface_texte, rect_texte)

    def est_clique(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                if self.rect.collidepoint(event.pos):
                    return True
        return False

def dessiner_regles(screen):
    screen.fill((50, 50, 50)) # Fond gris foncé
    largeur = screen.get_width()
    hauteur = screen.get_height()
    milieu_x = largeur // 2
    
    font_titre = pygame.font.Font(None, 60)
    font_desc = pygame.font.Font(None, 30)
    
    # Titre
    titre = font_titre.render("COMMENT JOUER ?", True, (255, 215, 0))
    screen.blit(titre, (largeur//2 - titre.get_width()//2, 30))

    # --- ZONE GAUCHE : CLAVIER ---
    pygame.draw.rect(screen, (100, 100, 200), (50, 100, milieu_x - 100, 400), 2)
    titre_j1 = font_desc.render("JOUEUR 1 (Clavier)", True, (200, 200, 255))
    screen.blit(titre_j1, (milieu_x//2 - titre_j1.get_width()//2, 110))

    # Dessin des touches ZSDE
    # Centre de la zone gauche
    cx, cy = 50 + (milieu_x - 100)//2, 100 + 200
    taille_touche = 60
    
    # Coordonnées relatives
    touches = [
        ("Z", cx - taille_touche, cy - taille_touche), # Haut Gauche
        ("E", cx + taille_touche, cy - taille_touche), # Haut Droite
        ("S", cx - taille_touche, cy + taille_touche), # Bas Gauche
        ("D", cx + taille_touche, cy + taille_touche)  # Bas Droite
    ]
    
    for lettre, tx, ty in touches:
        pygame.draw.rect(screen, (255, 255, 255), (tx-25, ty-25, 50, 50), border_radius=5)
        txt = font_desc.render(lettre, True, (0, 0, 0))
        screen.blit(txt, (tx - txt.get_width()//2, ty - txt.get_height()//2))

    expl_j1 = font_desc.render("Utilisez Z, S, D, E pour couper dans les zones", True, (200, 200, 200))
    screen.blit(expl_j1, (milieu_x//2 - expl_j1.get_width()//2, 520))

    # --- ZONE DROITE : SOURIS ---
    pygame.draw.rect(screen, (200, 100, 100), (milieu_x + 50, 100, milieu_x - 100, 400), 2)
    titre_j2 = font_desc.render("JOUEUR 2 / SOLO (Souris)", True, (255, 200, 200))
    screen.blit(titre_j2, (milieu_x + milieu_x//2 - titre_j2.get_width()//2, 110))
    
    # Dessin symbolique souris
    pygame.draw.ellipse(screen, (255, 255, 255), (milieu_x + milieu_x//2 - 30, 250, 60, 90), 3)
    pygame.draw.line(screen, (255, 255, 255), (milieu_x + milieu_x//2, 250), (milieu_x + milieu_x//2, 280), 3)
    
    expl_j2 = font_desc.render("Maintenez le clic gauche et glissez pour couper", True, (200, 200, 200))
    screen.blit(expl_j2, (milieu_x + milieu_x//2 - expl_j2.get_width()//2, 520))

def dessiner_scores(screen):
    screen.fill((50, 50, 50))
    font = pygame.font.Font(None, 50)
    titre = font.render("MEILLEURS SCORES", True, (255, 215, 0))
    screen.blit(titre, (screen.get_width()//2 - titre.get_width()//2, 50))

    try:
        with open('scores.json', 'r') as f:
            data = json.load(f)
            score_j1 = data.get('joueur1', 0)
            score_j2 = data.get('joueur2', 0)
    except:
        score_j1 = 0
        score_j2 = 0

    txt_s1 = font.render(f"Dernier Score Joueur 1 : {score_j1}", True, (255, 255, 255))
    txt_s2 = font.render(f"Dernier Score Joueur 2 : {score_j2}", True, (255, 255, 255))
    
    screen.blit(txt_s1, (screen.get_width()//2 - txt_s1.get_width()//2, 200))
    screen.blit(txt_s2, (screen.get_width()//2 - txt_s2.get_width()//2, 300))