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

# --- CHARGEMENT DES FONDS D'ÉCRAN ---
try:
    fond_joueur1_de_2 = pygame.image.load("Assets/Images/Backgrounds/Background1.png").convert()
    fond_joueur1 = pygame.image.load('Assets/Images/Backgrounds/Background2.png').convert()
    fond_joueur2 = pygame.image.load("Assets/Images/Backgrounds/Background3.png").convert()
    print("✓ Images de fond chargées avec succès")
except pygame.error as e:
    print(f"✗ Erreur chargement fond d'écran : {e}")
    fond_joueur1_de_2 = pygame.Surface((100, 100))
    fond_joueur1_de_2.fill((100, 50, 50)) 
    fond_joueur1 = pygame.Surface((100, 100))
    fond_joueur1.fill((50, 50, 100)) 
    fond_joueur2 = pygame.Surface((100, 100))
    fond_joueur2.fill((50, 50, 100)) 

# --- ETAT DU JEU ---
etat_jeu = "menu" 
nombre_de_joueurs = 1
start_ticks = 0 

# --- CRÉATION DES BOUTONS DU MENU (Initialisation) ---
# On les crée une première fois, mais leurs positions seront mises à jour dans la boucle
cx = L_ecran // 2
bouton_1j = Bouton(cx - 150, 150, 300, 60, "1 Joueur", (0, 100, 0), (0, 150, 0))
bouton_2j = Bouton(cx - 150, 230, 300, 60, "2 Joueurs", (0, 0, 100), (0, 0, 150))
bouton_regles = Bouton(cx - 150, 310, 300, 60, "Comment jouer", (100, 100, 0), (150, 150, 0))
bouton_scores = Bouton(cx - 150, 390, 300, 60, "Scores", (100, 0, 100), (150, 0, 150))
bouton_quitter = Bouton(cx - 150, 550, 300, 60, "Quitter", (100, 0, 0), (150, 0, 0))

bouton_retour = Bouton(20, 20, 150, 50, "Retour", (50, 50, 50), (100, 100, 100))

# Variables de jeu
mes_fruits = [] 
frequence_lancer = random.randint(30, 100)
compteur = 0
running = True

# --- BOUCLE PRINCIPALE ---
while running: 
    
    # ===============================================================
    # 0. RE-CENTRAGE DYNAMIQUE (POUR LE PLEIN ÉCRAN)
    # ===============================================================
    # On calcule le centre actuel de la fenêtre
    largeur_actuelle = screen.get_width()
    centre_x = largeur_actuelle // 2
    
    # On met à jour la position X (rectangle) des boutons pour les centrer
    # On suppose que vos boutons ont un attribut 'rect' (standard Pygame)
    bouton_1j.rect.centerx = centre_x
    bouton_2j.rect.centerx = centre_x
    bouton_regles.rect.centerx = centre_x
    bouton_scores.rect.centerx = centre_x
    bouton_quitter.rect.centerx = centre_x
    # ===============================================================

    # 1. GESTION DES ÉVÉNEMENTS
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        # Gestion du basculement Plein Écran avec F11 ou F
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f or event.key == pygame.K_F11:
                # Bascule entre plein écran et fenêtré
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # --- ÉVÉNEMENTS DU MENU ---
        if etat_jeu == "menu":
            if bouton_1j.est_clique(event):
                nombre_de_joueurs = 1
                etat_jeu = "jeu"
                mes_fruits = [] 
                start_ticks = pygame.time.get_ticks() 
                
            if bouton_2j.est_clique(event):
                nombre_de_joueurs = 2
                etat_jeu = "jeu"
                mes_fruits = []
                start_ticks = pygame.time.get_ticks()

            if bouton_regles.est_clique(event):
                etat_jeu = "regles"
            if bouton_scores.est_clique(event):
                etat_jeu = "scores"
            if bouton_quitter.est_clique(event):
                running = False

        elif etat_jeu in ["regles", "scores"]:
            if bouton_retour.est_clique(event):
                etat_jeu = "menu"

        # --- ÉVÉNEMENTS DU JEU ---
        elif etat_jeu == "jeu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                etat_jeu = "menu"
                mes_fruits = [] 

            # Calcul du temps écoulé
            seconds_ecoules = (pygame.time.get_ticks() - start_ticks) / 1000
            
            # Inputs seulement si le décompte est fini
            if seconds_ecoules > 3:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    controller.start_slice(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONUP:
                    controller.end_slice(mes_fruits, screen.get_width(), nombre_de_joueurs)
                if event.type == pygame.KEYDOWN:
                    controller.handle_keyboard_inputs(mes_fruits, screen.get_width(), screen.get_height(), event.key, nombre_de_joueurs)

    # 2. LOGIQUE ET DESSIN SELON L'ÉTAT
    
    if etat_jeu == "menu":
        screen.fill((30, 30, 40))
        font_titre = pygame.font.Font(None, 80)
        titre = font_titre.render("FRUIT SLICER", True, (255, 100, 100))
        
        # Le titre aussi doit être centré dynamiquement
        screen.blit(titre, (screen.get_width()//2 - titre.get_width()//2, 50))
        
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
        
        seconds_ecoules = (pygame.time.get_ticks() - start_ticks) / 1000
        en_attente = seconds_ecoules < 3  

        # --- LOGIQUE DU JEU ---
        if not en_attente:
            if not en_attente:
                if controller.slicing:
                    # On passe maintenant mes_fruits pour vérifier la coupe en temps réel
                    controller.update_slice(pygame.mouse.get_pos(), mes_fruits, screen.get_width(), nombre_de_joueurs)
            
            compteur += 1
            if compteur >= frequence_lancer:
                type_fruit = random.choice(liste_fruits)
                if nombre_de_joueurs == 2:
                    zone_joueur = random.choice([1, 2])
                else:
                    zone_joueur = None 
                    
                mes_fruits.append(Fruit(type_fruit, screen.get_width(), screen.get_height(), zone_joueur))
                compteur = 0
                frequence_lancer = random.randint(30, 100)

        # --- AFFICHAGE (FONDS + TEXTES INFORMATIFS) ---
        largeur_ecran = screen.get_width()
        hauteur_ecran = screen.get_height()
        milieu_x = largeur_ecran // 2
        font_info = pygame.font.Font(None, 40)

        if nombre_de_joueurs == 1:
            bg_scaled = pygame.transform.scale(fond_joueur1, (largeur_ecran, hauteur_ecran))
            screen.blit(bg_scaled, (0, 0))
            
            txt_info = font_info.render("Clavier ou Souris", True, (255, 255, 255))
            screen.blit(txt_info, (largeur_ecran//2 - txt_info.get_width()//2, 20))

        else:
            bg_left = pygame.transform.scale(fond_joueur1_de_2, (milieu_x, hauteur_ecran))
            screen.blit(bg_left, (0, 0))
            bg_right = pygame.transform.scale(fond_joueur2, (milieu_x, hauteur_ecran))
            screen.blit(bg_right, (milieu_x, 0))
            
            pygame.draw.line(screen, (255, 255, 255), (milieu_x, 0), (milieu_x, hauteur_ecran), 3)
            
            t1 = font_info.render("J1 (Clavier)", True, (255, 255, 255))
            t2 = font_info.render("J2 (Souris)", True, (255, 255, 255))
            screen.blit(t1, (milieu_x//2 - t1.get_width()//2, 20))
            screen.blit(t2, (milieu_x + milieu_x//2 - t2.get_width()//2, 20))

        # Affichage des fruits
        for f in mes_fruits:
            if not en_attente:
                f.update(screen.get_width())
            f.draw(screen)

        if not en_attente:
            controller.draw_slice(screen)
            mes_fruits = [f for f in mes_fruits if f.y < screen.get_height() + 100]

        # --- AFFICHAGE DU DÉCOMPTE ---
        if en_attente:
            chiffre = int(4 - seconds_ecoules)
            font_phrase = pygame.font.Font(None, 45)
            font_chrono = pygame.font.Font(None, 150)
            
            surf_phrase = font_phrase.render("Le jeu démarre dans", True, (255, 255, 255))
            surf_chrono = font_chrono.render(str(chiffre), True, (255, 215, 0))
            
            if nombre_de_joueurs == 1:
                rect_phrase = surf_phrase.get_rect(center=(largeur_ecran//2, hauteur_ecran//2 - 60))
                rect_chrono = surf_chrono.get_rect(center=(largeur_ecran//2, hauteur_ecran//2 + 40))
                screen.blit(surf_phrase, rect_phrase)
                screen.blit(surf_chrono, rect_chrono)
            else:
                rect_phrase_j1 = surf_phrase.get_rect(center=(milieu_x//2, hauteur_ecran//2 - 60))
                rect_chrono_j1 = surf_chrono.get_rect(center=(milieu_x//2, hauteur_ecran//2 + 40))
                
                rect_phrase_j2 = surf_phrase.get_rect(center=(milieu_x + milieu_x//2, hauteur_ecran//2 - 60))
                rect_chrono_j2 = surf_chrono.get_rect(center=(milieu_x + milieu_x//2, hauteur_ecran//2 + 40))
                
                screen.blit(surf_phrase, rect_phrase_j1)
                screen.blit(surf_chrono, rect_chrono_j1)
                screen.blit(surf_phrase, rect_phrase_j2)
                screen.blit(surf_chrono, rect_chrono_j2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()