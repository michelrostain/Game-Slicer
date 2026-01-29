import pygame,random
from constantes import liste_fruits, images, load_assets
import controller
from objets import Fruit


# INITIALISATION DE PYGAME :
################################
# Initialise toutes les biblipthèques de Pygame, ainsi que le son
pygame.init()

L_ecran=1280
H_ecran=720

# Variable screen qui devient la fenêtre principale du jeu
screen=pygame.display.set_mode((L_ecran, H_ecran), pygame.RESIZABLE)

# Taille écran par joueur
largeur_joueur=L_ecran //2 

# CREATION DES DEUX ECRANS
#################################
rect_gauche=pygame.Rect(0, 0, largeur_joueur, H_ecran)
rect_droite=pygame.Rect(largeur_joueur, 0, largeur_joueur, H_ecran)

ecran_gauche=screen.subsurface(rect_gauche)
ecran_droite=screen.subsurface(rect_droite)
#################################


# Objet horloge qui permet de gérer le nombre d'image par seconde du jeu
clock=pygame.time.Clock()

# Variable pour définir quand le jeu est actif
running=True

load_assets()
lancement_fruit=True

fruit_choisi=random.choice(liste_fruits)
# Gestionnaire d'existence des fruits crées et envoyés, pour un apparition simultanée de plusieurs fruits
mes_fruits = [] 
fruits_j1=[]
fruits_j2=[]

frequence_lancer = random.randint(20, 60)
compteur=0

while running : 
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running=False

        # Souris : slicing par traînée
        if event.type == pygame.MOUSEBUTTONDOWN:
            controller.start_slice(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            controller.end_slice(mes_fruits)
        
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
    
    compteur+=1
    if compteur >= frequence_lancer:
        # Lancement fruits pour le joueur1
        fruit_choisi_1 = random.choice(liste_fruits)
        nouveau_f1=(Fruit(fruit_choisi_1, ecran_gauche.get_width(), ecran_gauche.get_height()))
        fruits_j1.append(nouveau_f1)

        # Lancement fruits pour le joueur2
        fruit_choisi_2 = random.choice(liste_fruits)
        nouveau_f2=(Fruit(fruit_choisi_2, ecran_droite.get_width(), ecran_droite.get_height()))
        fruits_j2.append(nouveau_f2)

        compteur=0
        # Apparition des fruits plus naturelle
        frequence_lancer = random.randint(30, 100)

    ecran_gauche.fill("purple")
    ecran_droite.fill("blue")

    for f in fruits_j1:
        f.update(ecran_gauche.get_width())  # Mise à jour du déplacement en fonction des frames pour le joueur1
        f.draw(ecran_gauche)

    for f in fruits_j2:
        f.update(ecran_droite.get_width())  # Mise à jour du déplacement en fonction des frames pour le joueur2
        f.draw(ecran_droite)


    # Dessine la trainée par-dessus des fruits
    controller.draw_slice(screen)
    
    # Nettoyage des fruits hors écran (en bas)
    mes_fruits=[f for f in mes_fruits if f.y < screen.get_height() + 100 ]

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

