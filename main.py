import pygame,random
from constantes import liste_fruits, images, load_assets
import controller
from objets import Fruit


# INITIALISATION DE PYGAME :
################################
# Initialise toutes les biblipthèques de Pygame, ainsi que le son
pygame.init()

# Variable screen qui devient la fenêtre principale du jeu
screen=pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

# Objet horloge qui permet de gérer le nombre d'image par seconde du jeu
clock = pygame.time.Clock()

# Variable pour définir quand le jeu est actif
running=True
################################
load_assets()

# Variables de jeu
# Gestionnaire d'existence des fruits crées et envoyés, pour un apparition simultanée de plusieurs fruits
mes_fruits = [] 
frequence_lancer = random.randint(30, 100)
compteur=0

# Boucle principale du jeu
while running : 
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running=False

        # Souris : slicing par traînée
        if event.type == pygame.MOUSEBUTTONDOWN:
            controller.start_slice(pygame.mouse.get_pos())
            
        if event.type == pygame.MOUSEBUTTONUP:
            controller.end_slice(mes_fruits, screen.get_width())
        
        if event.type == pygame.KEYDOWN :
            # Si on  presse r, la fenêtre devient réglable
            if event.key == pygame.K_r:
                screen=pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
            if event.key == pygame.K_f:
                screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Gestion du slicing par zones clavier
            controller.handle_keyboard_inputs(mes_fruits, screen.get_width(), screen.get_height(), event.key)

    # Mise à jour de la traînée si on slice (une fois par frame)
    if controller.slicing:
        controller.update_slice(pygame.mouse.get_pos())
    
    # Génération de nouveaux fruits
    compteur+=1
    if compteur >= frequence_lancer:
        zone_joueur = random.choice([1,2])
        mes_fruits.append(Fruit(zone_joueur, screen.get_width(), screen.get_height(), zone_joueur))
        compteur=0
        # Apparition des fruits plus naturelle
        frequence_lancer = random.randint(30, 100)

    # Affichage
    screen.fill("purple")

    # ============================================
    # DIVISION DE L'ÉCRAN EN 2 (MODE 2 JOUEURS)
    # ============================================
    largeur_ecran = screen.get_width()
    hauteur_ecran = screen.get_height()
    milieu_x = largeur_ecran // 2
    
    # Ligne verticale au milieu pour séparer les 2 zones
    pygame.draw.line(screen, (255, 255, 255), (milieu_x, 0), (milieu_x, hauteur_ecran), 3)
    
    # Texte pour indiquer les zones des joueurs
    font = pygame.font.Font(None, 36)
    texte_j1 = font.render("JOUEUR 1 (Clavier)", True, (255, 255, 255))
    texte_j2 = font.render("JOUEUR 2 (Souris)", True, (255, 255, 255))
    screen.blit(texte_j1, (milieu_x // 2 - texte_j1.get_width() // 2, 20))
    screen.blit(texte_j2, (milieu_x + milieu_x // 2 - texte_j2.get_width() // 2, 20))
    # ============================================

    # Mise à jour et affichage des fruits
    for f in mes_fruits:
        f.update(screen.get_width())  # Mise à jour du déplacement en fonction des frames
        f.draw(screen)

    # Dessine la trainée par-dessus des fruits
    controller.draw_slice(screen)
    
    # Nettoyage des fruits hors écran (en bas)
    mes_fruits=[f for f in mes_fruits if f.y < screen.get_height() + 100 ]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

