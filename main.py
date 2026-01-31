import pygame, random
from constantes import liste_fruits, images, load_assets
import controller
from objets import Fruit, Glacon
from interface import Bouton, dessiner_regles, dessiner_scores

# INITIALISATION
pygame.init()
L_ecran = 1280
H_ecran = 720
screen = pygame.display.set_mode((L_ecran, H_ecran), pygame.RESIZABLE)
pygame.display.set_caption("Fruit Slicer")
clock = pygame.time.Clock()
load_assets()

# --- CHARGEMENT DES FONDS ---
try:
    fond_joueur1_de_2 = pygame.image.load("Assets/Images/Backgrounds/Background1.png").convert()
    fond_joueur1 = pygame.image.load('Assets/Images/Backgrounds/Background2.png').convert()
    fond_joueur2 = pygame.image.load("Assets/Images/Backgrounds/Background3.png").convert()
except pygame.error:
    # Fonds de secours
    fond_joueur1_de_2 = pygame.Surface((100, 100)); fond_joueur1_de_2.fill((100, 50, 50)) 
    fond_joueur1 = pygame.Surface((100, 100)); fond_joueur1.fill((50, 50, 100)) 
    fond_joueur2 = pygame.Surface((100, 100)); fond_joueur2.fill((50, 50, 100)) 

# --- ETAT DU JEU ---
etat_jeu = "menu" 
nombre_de_joueurs = 1
start_ticks = 0 

# NOUVEAU : Vies séparées
vies_j1 = 3
vies_j2 = 3

# --- BOUTONS ---
cx = L_ecran // 2
bouton_1j = Bouton(cx - 150, 150, 300, 60, "1 Joueur", (0, 100, 0), (0, 150, 0))
bouton_2j = Bouton(cx - 150, 230, 300, 60, "2 Joueurs", (0, 0, 100), (0, 0, 150))
bouton_regles = Bouton(cx - 150, 310, 300, 60, "Comment jouer", (100, 100, 0), (150, 150, 0))
bouton_scores = Bouton(cx - 150, 390, 300, 60, "Scores", (100, 0, 100), (150, 0, 150))
bouton_quitter = Bouton(cx - 150, 550, 300, 60, "Quitter", (100, 0, 0), (150, 0, 0))
bouton_retour = Bouton(20, 20, 150, 50, "Retour", (50, 50, 50), (100, 100, 100))
bouton_menu_go = Bouton(0, 0, 300, 60, "Menu Principal", (100, 100, 100), (150, 150, 150))

# Variables de jeu
mes_fruits = [] 
frequence_lancer = random.randint(30, 100)
compteur = 0
running = True
niveau = 1
score = 0
gravite_actuelle = 0.4

# Gestion du son
try:
    # Un seul fichier qui contient "3... 2... 1... GO!"
    son_decompte = pygame.mixer.Sound("Assets/Sounds/decompte_complet.wav")
    son_decompte.set_volume(0.6)
except (pygame.error, FileNotFoundError):
    print("Son manquant, création d'un son vide.")
    son_decompte = pygame.mixer.Sound(buffer=bytearray())

# --- BOUCLE PRINCIPALE ---
while running: 
    
    # 0. RE-CENTRAGE DYNAMIQUE
    largeur_actuelle = screen.get_width()
    centre_x = largeur_actuelle // 2
    
    bouton_1j.rect.centerx = centre_x
    bouton_2j.rect.centerx = centre_x
    bouton_regles.rect.centerx = centre_x
    bouton_scores.rect.centerx = centre_x
    bouton_quitter.rect.centerx = centre_x
    bouton_menu_go.rect.centerx = centre_x
    bouton_menu_go.rect.y = screen.get_height() // 2 + 120

    # 1. GESTION DES ÉVÉNEMENTS
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f or event.key == pygame.K_F11:
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        if etat_jeu == "menu":
            if bouton_1j.est_clique(event):
                nombre_de_joueurs = 1
                etat_jeu = "jeu"
                mes_fruits = []
                # Réinitialisation
                vies_j1 = 3 
                start_ticks = pygame.time.get_ticks() 
                
                # Reset des variables de niveau pour un nouveau jeu
                niveau = 1
                score = 0
                gravite_actuelle = 0.4 

                son_decompte.stop() # Coupe le son s'il jouait déjà
                son_decompte.play()
                
            if bouton_2j.est_clique(event):
                nombre_de_joueurs = 2
                etat_jeu = "jeu"
                mes_fruits = []
                # Réinitialisation des DEUX joueurs
                vies_j1 = 3
                vies_j2 = 3
                start_ticks = pygame.time.get_ticks()

                son_decompte.stop() # Coupe le son s'il jouait déjà
                son_decompte.play()

            if bouton_regles.est_clique(event): etat_jeu = "regles"
            if bouton_scores.est_clique(event): etat_jeu = "scores"
            if bouton_quitter.est_clique(event): running = False

        elif etat_jeu in ["regles", "scores"]:
            if bouton_retour.est_clique(event): etat_jeu = "menu"
        
        elif etat_jeu == "game_over":
            if bouton_menu_go.est_clique(event):
                etat_jeu = "menu"

        elif etat_jeu == "jeu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                etat_jeu = "menu"
                mes_fruits = [] 
                son_decompte.stop()

            seconds_ecoules = (pygame.time.get_ticks() - start_ticks) / 1000
            
            if seconds_ecoules > 3:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    controller.start_slice(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONUP:
                    controller.end_slice(mes_fruits, screen.get_width(), nombre_de_joueurs)
                if event.type == pygame.KEYDOWN:
                    controller.handle_keyboard_inputs(mes_fruits, screen.get_width(), screen.get_height(), event.key, nombre_de_joueurs)

    # 2. LOGIQUE ET DESSIN
    
    if etat_jeu == "menu":
        screen.fill((30, 30, 40))
        font_titre = pygame.font.Font(None, 80)
        titre = font_titre.render("FRUIT SLICER", True, (255, 100, 100))
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

    # --- ÉCRAN GAME OVER (LOGIQUE MODIFIÉE) ---
    elif etat_jeu == "game_over":
        screen.fill((20, 0, 0)) # Fond rouge sombre général
        
        milieu_x = screen.get_width() // 2
        
        # Ligne de séparation pour garder la cohérence visuelle
        if nombre_de_joueurs == 2:
            pygame.draw.line(screen, (100, 0, 0), (milieu_x, 0), (milieu_x, screen.get_height()), 2)

        font_go = pygame.font.Font(None, 80)
        font_raison = pygame.font.Font(None, 40)
        
        txt_go = font_go.render("GAME OVER", True, (255, 0, 0))
        txt_perdu = font_raison.render("Vous avez perdu !", True, (200, 200, 200))
        txt_gagne = font_go.render("VAINQUEUR !", True, (0, 255, 0))

        if nombre_de_joueurs == 1:
            # Affichage classique centré
            screen.blit(txt_go, (screen.get_width()//2 - txt_go.get_width()//2, screen.get_height()//2 - 100))
        else:
            # --- LOGIQUE GAME OVER 2 JOUEURS ---
            
            # Affichage pour le Joueur 1 (Gauche)
            if vies_j1 <= 0:
                # J1 a perdu
                screen.blit(txt_go, (milieu_x//2 - txt_go.get_width()//2, screen.get_height()//2 - 100))
                screen.blit(txt_perdu, (milieu_x//2 - txt_perdu.get_width()//2, screen.get_height()//2 - 20))
            else:
                # J1 a gagné (car le jeu s'arrête si l'un perd)
                screen.blit(txt_gagne, (milieu_x//2 - txt_gagne.get_width()//2, screen.get_height()//2 - 100))

            # Affichage pour le Joueur 2 (Droite)
            if vies_j2 <= 0:
                # J2 a perdu
                screen.blit(txt_go, (milieu_x + milieu_x//2 - txt_go.get_width()//2, screen.get_height()//2 - 100))
                screen.blit(txt_perdu, (milieu_x + milieu_x//2 - txt_perdu.get_width()//2, screen.get_height()//2 - 20))
            else:
                # J2 a gagné
                screen.blit(txt_gagne, (milieu_x + milieu_x//2 - txt_gagne.get_width()//2, screen.get_height()//2 - 100))

        bouton_menu_go.dessiner(screen)

    # --- ÉCRAN DE JEU ---
    elif etat_jeu == "jeu":
        
        seconds_ecoules = (pygame.time.get_ticks() - start_ticks) / 1000
        en_attente = seconds_ecoules < 3  

        # --- LOGIQUE ---
        if not en_attente:
            if controller.slicing:
                result = controller.update_slice(pygame.mouse.get_pos(), mes_fruits, screen.get_width(), nombre_de_joueurs)
                if result == 1 and nombre_de_joueurs == 1:
                    score += 1
                    # Gestion de la montée de niveau tous les 10 points
                    if score > 0 and score % 10 == 0:
                        niveau += 1
                        # Augmentation de la gravité
                        gravite_actuelle = (min(0.4 + (niveau - 1) * 0.03, 1.0))
                elif result == "freeze" and nombre_de_joueurs == 1:
                    # Activer l'effet de freeze à partir du niveau 3
                    if niveau >= 3:
                        vies_j1 -= 1
                        if vies_j1 <= 0:
                            etat_jeu = "game_over"
            
            compteur += 1
            # Ajustement de la fréquence en fonction du niveau (uniquement en mode 1 joueur)
            if nombre_de_joueurs == 1:
                min_freq = max(20, 50 - (niveau - 1) * 2)  # Fréquence minimale diminue avec le niveau
                max_freq = max(40, 150 - (niveau - 1) * 3)  # Maximale aussi
            else:
                min_freq = 30  # Valeurs par défaut pour mode 2 joueurs
                max_freq = 100
            if compteur >= frequence_lancer:
                # 1 chance sur 10 de faire apparaître un Glaçon (dans les deux modes)
                if random.randint(1, 10) == 1:
                    # On crée un glaçon
                    mes_fruits.append(Glacon(screen.get_width(), screen.get_height(), gravite_actuelle if nombre_de_joueurs == 1 else 0.4))
                else:
                    # Sinon, on crée un fruit normal (Code d'avant)
                    type_fruit = random.choice(liste_fruits)
                    if nombre_de_joueurs == 2:
                        zone_joueur = random.choice([1, 2])
                    else:
                        zone_joueur = None
                    
                    # Passer la gravité actuelle uniquement si mode 1 joueur, sinon défaut
                    gravite_pour_fruit = gravite_actuelle if nombre_de_joueurs == 1 else 0.4
                    mes_fruits.append(Fruit(type_fruit, screen.get_width(), screen.get_height(), zone_joueur, gravite_pour_fruit))
                compteur = 0
                frequence_lancer = random.randint(min_freq, max_freq)

        # --- AFFICHAGE FONDS ---
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

        # --- GESTION FRUITS ET VIES SÉPARÉES ---
        for f in mes_fruits[:]:
            if not en_attente:
                f.update(screen.get_width())
            f.draw(screen)

            # --- DÉTECTION FRUIT RATÉ ---
            if f.y > screen.get_height() + 50: 
                mes_fruits.remove(f)
                
                if not f.sliced and not en_attente:
                    if nombre_de_joueurs == 1:
                        # Mode 1 joueur : on utilise vies_j1 par défaut
                        vies_j1 -= 1
                        if vies_j1 <= 0:
                            etat_jeu = "game_over"
                    else:
                        # Mode 2 joueurs : on regarde le côté
                        if f.x < milieu_x:
                            # C'est un fruit de GAUCHE (Joueur 1)
                            vies_j1 -= 1
                            print(f"J1 a raté ! Vies restantes : {vies_j1}")
                        else:
                            # C'est un fruit de DROITE (Joueur 2)
                            vies_j2 -= 1
                            print(f"J2 a raté ! Vies restantes : {vies_j2}")
                        
                        # Si l'un des deux meurt, c'est Game Over global
                        if vies_j1 <= 0 or vies_j2 <= 0:
                            etat_jeu = "game_over"

        if not en_attente:
            controller.draw_slice(screen)

        # --- AFFICHAGE DES VIES (HUD) ---
        font_vies = pygame.font.Font(None, 50)
        
        if nombre_de_joueurs == 1:
            txt_vies = font_vies.render(f"VIES : {vies_j1}", True, (255, 0, 0))
            screen.blit(txt_vies, (largeur_ecran // 2 - txt_vies.get_width() // 2, 70))
            txt_niveau = font_vies.render(f"NIVEAU : {niveau}", True, (255, 255, 0))
            screen.blit(txt_niveau, (largeur_ecran // 2 - txt_niveau.get_width() // 2, 120))
        else:
            # Vies J1 (Gauche)
            txt_vies_j1 = font_vies.render(f"VIES : {vies_j1}", True, (255, 0, 0))
            screen.blit(txt_vies_j1, (milieu_x // 2 - txt_vies_j1.get_width() // 2, 70))
            
            # Vies J2 (Droite)
            txt_vies_j2 = font_vies.render(f"VIES : {vies_j2}", True, (255, 0, 0))
            screen.blit(txt_vies_j2, (milieu_x + milieu_x // 2 - txt_vies_j2.get_width() // 2, 70))


        # --- DÉCOMPTE DÉBUT DE JEU ---
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