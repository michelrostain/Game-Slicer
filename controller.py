import pygame
import math
from objets import Glacon, Bombe

# Variables pour le slicing à la souris
slicing = False
slice_points = []

def start_slice(mouse_pos):
    """
    Démarre le slicing à la position de la souris
    """
    global slicing, slice_points
    slicing = True
    slice_points = [mouse_pos]

def update_slice(mouse_pos, mes_fruits, screen_width, nombre_de_joueurs=1):
    """
    Met à jour la traînée ET vérifie les collisions en temps réel (sous le curseur)
    """
    global slice_points
    
    if slicing:
        # 1. Mise à jour visuelle (La traînée "pour faire joli")
        slice_points.append(mouse_pos)
        # On garde seulement les 15 derniers points pour éviter une traînée infinie
        if len(slice_points) > 15:
            slice_points.pop(0)

        # 2. LOGIQUE DE TRANCHAGE (Le pointeur coupe le fruit)
        mx, my = mouse_pos
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
            distance = math.sqrt((mx - fruit.x)**2 + (my - fruit.y)**2)
            
            if distance < fruit.radius:
                # Vérifie qu'on ne coupe pas un fruit déjà coupé
                if not fruit.sliced: 
                    
                    # DÉTECTION DU TYPE
                    if isinstance(fruit, Glacon) or fruit.type == "glacon":
                        mes_fruits.remove(fruit) # Le glaçon disparait
                        return "freeze"
                    if isinstance(fruit, Bombe) or fruit.type == "bombe":
                        mes_fruits.remove(fruit) # La bombe disparait
                        return "game_over"
                    
                    # SI C'EST UNE POIRE (ou fruit à états)
                    elif fruit.images_set:
                        fruit.couper() # On change l'image, MAIS on ne remove pas
                        # Le fruit va continuer de tomber avec l'image "cut"
                        # On retourne 1 pour incrémenter le score
                        return 1 
                    
                    # SI C'EST UN FRUIT NORMAL (Pomme standard)
                    else:
                        mes_fruits.remove(fruit) # On supprime direct
                        return 1  # On retourne 1 pour incrémenter le score
def end_slice(mes_fruits, screen_width=None, nombre_de_joueurs=1):
    """
    Termine le slicing.
    Désormais, cette fonction ne sert qu'à arrêter le dessin de la traînée.
    La coupe a déjà été faite dans update_slice.
    """
    global slicing, slice_points
    slicing = False
    slice_points = []

def handle_keyboard_inputs(mes_fruits, screen_width, screen_height, key, nombre_de_joueurs=1):
    """
    Gestion du Joueur 1 (Clavier)
    """
    milieu_x = screen_width // 2
    bonus_active = None
    
    # Définition des 4 zones du joueur 1 (Gauche)
    # Format: (x_min, y_min, x_max, y_max)
    zones = {
        pygame.K_z: (0, 0, milieu_x // 2, screen_height // 2),                     # Haut-gauche
        pygame.K_s: (0, screen_height // 2, milieu_x // 2, screen_height),         # Bas-gauche
        pygame.K_d: (milieu_x // 2, screen_height // 2, milieu_x, screen_height),  # Bas-droite (de la zone J1)
        pygame.K_e: (milieu_x // 2, 0, milieu_x, screen_height // 2)               # Haut-droite (de la zone J1)
    }
    
    if key in zones:
        zone = zones[key]
        sliced = 0
        for fruit in mes_fruits[:]: 
            # Le fruit est-il dans la zone activée par la touche ?
            if zone[0] <= fruit.x <= zone[2] and zone[1] <= fruit.y <= zone[3]:
                # Sécurité : on vérifie qu'il est bien dans la moitié gauche globale
                if isinstance(fruit, Bombe) or fruit.type == "bombe":
                    mes_fruits.remove(fruit)
                    print("[J1 CLAVIER] Bombe tranchée ! GAME OVER !")
                    bonus_active = "game_over"
                elif isinstance(fruit, Glacon) or fruit.type == "glacon":
                    mes_fruits.remove(fruit)
                    print("[J1 CLAVIER] Glaçon tranché ! Temps gelé !")
                    bonus_active = "freeze"
                    
                elif fruit.images_set:
                    fruit.couper()
                    sliced += 1
                
                else:
                    mes_fruits.remove(fruit)
                    sliced += 1
        
        if sliced > 0:
            print(f"[J1 CLAVIER] {sliced} fruit(s) slicé(s) !")
    return bonus_active

def draw_slice(screen):
    """Dessine la traînée visuelle"""
    if slicing and len(slice_points) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, slice_points, 3)