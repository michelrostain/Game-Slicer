import pygame, random
from constantes import liste_fruits, images, load_assets
import controller
from objets import Fruit
# Importation de notre nouveau fichier interface
from interface import Bouton, dessiner_regles, dessiner_scores

# INITIALISATION
pygame.init()
L_ecran = 1280
H_ecran = 720
screen = pygame.display.set_mode((L_ecran, H_ecran), pygame.RESIZABLE)
pygame.display.set_caption("Fruit Slicer - Menu")
clock = pygame.time.Clock()
load_assets()

# --- ETAT DU JEU ---
# "menu", "jeu", "regles", "scores"
etat_jeu = "menu" 
nombre_de_joueurs = 1

# --- CRÉATION DES BOUTONS DU MENU ---
# Centrés horizontalement
cx = L_ecran // 2
bouton_1j = Bouton(cx - 150, 150, 300, 60, "1 Joueur", (0, 100, 0), (0, 150, 0))
bouton_2j = Bouton(cx - 150, 230, 300, 60, "2 Joueurs", (0, 0, 100), (0, 0, 150))
bouton_regles = Bouton(cx - 150, 310, 300, 60, "Comment jouer", (100, 100, 0), (150, 150, 0))
bouton_scores = Bouton(cx - 150, 390, 300, 60, "Scores", (100, 0, 100), (150, 0, 150))
bouton_quitter = Bouton(cx - 150, 550, 300, 60, "Quitter", (100, 0, 0), (150, 0, 0))

# Bouton retour (utilisé dans les sous-menus)
bouton_retour = Bouton(20, 20, 150, 50, "Retour", (50, 50, 50), (100, 100, 100))

# Variables de jeu
mes_fruits = [] 
frequence_lancer = random.randint(30, 100)
compteur = 0
running = True

# --- BOUCLE PRINCIPALE ---
while running: 
    
    # 1. GESTION DES ÉVÉNEMENTS
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # --- ÉVÉNEMENTS DU MENU ---
        if etat_jeu == "menu":
            if bouton_1j.est_clique(event):
                nombre_de_joueurs = 1
                etat_jeu = "jeu"
                mes_fruits = [] # Reset fruits
            if bouton_2j.est_clique(event):
                nombre_de_joueurs = 2
                etat_jeu = "jeu"
                mes_fruits = []
            if bouton_regles.est_clique(event):
                etat_jeu = "regles"
            if bouton_scores.est_clique(event):
                etat_jeu = "scores"
            if bouton_quitter.est_clique(event):
                running = False

        # --- ÉVÉNEMENTS DES SOUS-MENUS ---
        elif etat_jeu in ["regles", "scores"]:
            if bouton_retour.est_clique(event):
                etat_jeu = "menu"

        # --- ÉVÉNEMENTS DU JEU ---
        elif etat_jeu == "jeu":
            # Touche Echap pour revenir au menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                etat_jeu = "menu"
                mes_fruits = [] # Nettoyer le jeu

            # Gestion Souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                controller.start_slice(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                # Ajout de l'argument nombre_de_joueurs
                controller.end_slice(mes_fruits, screen.get_width(), nombre_de_joueurs)
            
            # Gestion Clavier
            if event.type == pygame.KEYDOWN:
                # Ajout de l'argument nombre_de_joueurs
                controller.handle_keyboard_inputs(mes_fruits, screen.get_width(), screen.get_height(), event.key, nombre_de_joueurs)

    # 2. LOGIQUE ET DESSIN SELON L'ÉTAT
    
    if etat_jeu == "menu":
        screen.fill((30, 30, 40)) # Fond sombre
        # Titre
        font_titre = pygame.font.Font(None, 80)
        titre = font_titre.render("FRUIT SLICER", True, (255, 100, 100))
        screen.blit(titre, (L_ecran//2 - titre.get_width()//2, 50))
        
        # Dessiner les boutons
        bouton_1j.dessiner(screen)
        bouton_2j.dessiner(screen)
        bouton_regles.dessiner(screen)
        bouton_scores.dessiner(screen)
        bouton_quitter.dessiner(screen)

    elif etat_jeu == "regles":
        dessiner_regles(screen)
        bouton_retour.dessiner(screen)
        
    elif etat_jeu == "scores":
        dessiner_scores(screen)
        bouton_retour.dessiner(screen)

    elif etat_jeu == "jeu":
        # --- LOGIQUE DU JEU ---
        if controller.slicing:
            controller.update_slice(pygame.mouse.get_pos())
        
        compteur += 1
        if compteur >= frequence_lancer:
            type_fruit = random.choice(liste_fruits)
            # Spawn dynamique selon joueurs
            if nombre_de_joueurs == 2:
                zone_joueur = random.choice([1, 2])
            else:
                zone_joueur = None 
                
            mes_fruits.append(Fruit(type_fruit, screen.get_width(), screen.get_height(), zone_joueur))
            compteur = 0
            frequence_lancer = random.randint(30, 100)

        # --- AFFICHAGE DU JEU ---
        screen.fill("purple")
        
        largeur_ecran = screen.get_width()
        milieu_x = largeur_ecran // 2
        
        if nombre_de_joueurs == 2:
            pygame.draw.line(screen, (255, 255, 255), (milieu_x, 0), (milieu_x, screen.get_height()), 3)
            font = pygame.font.Font(None, 36)
            t1 = font.render("J1 (Clavier)", True, (255, 255, 255))
            t2 = font.render("J2 (Souris)", True, (255, 255, 255))
            screen.blit(t1, (milieu_x//2 - t1.get_width()//2, 20))
            screen.blit(t2, (milieu_x + milieu_x//2 - t2.get_width()//2, 20))

        for f in mes_fruits:
            f.update(screen.get_width())
            f.draw(screen)

        controller.draw_slice(screen)
        
        # Nettoyage
        mes_fruits = [f for f in mes_fruits if f.y < screen.get_height() + 100]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()