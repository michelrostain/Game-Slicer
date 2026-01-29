import pygame
import json
import math

# Variables pour le slicing à la souris
slicing = False
slice_points = []

def start_slice(mouse_pos):
    """
    Démarre le slicing à la position de la souris
    ZONE JOUEUR 2 : Fonctionne UNIQUEMENT sur la moitié DROITE de l'écran
    """
    global slicing, slice_points
    slicing = True
    slice_points = [mouse_pos]

def update_slice(mouse_pos):
    """Ajoute des points à la traînée pendant le slicing"""
    global slice_points
    if slicing:
        slice_points.append(mouse_pos)

def end_slice(mes_fruits, screen_width=None):
    """
    Termine le slicing et vérifie les collisions avec les fruits
    ZONE JOUEUR 2 : Ne slice QUE les fruits dans la moitié DROITE de l'écran
    """
    global slicing, slice_points
    if slicing:
        # Calcul du milieu de l'écran
        if screen_width is None:
            # Essaie de récupérer la largeur de l'écran
            surface = pygame.display.get_surface()
            if surface:
                screen_width = surface.get_width()
            else:
                screen_width = 1280  # Valeur par défaut
        
        milieu_x = screen_width // 2
        
        # Vérifie les collisions avec la ligne tracée
        sliced_fruits = []
        for fruit in mes_fruits:
            # ==========================================
            # RESTRICTION ZONE JOUEUR 2 (MOITIÉ DROITE)
            # ==========================================
            if fruit.x >= milieu_x:  # Fruit dans la zone droite uniquement
                if line_intersects_fruit(slice_points, fruit):
                    sliced_fruits.append(fruit)
        
        # Supprime les fruits slicés
        for fruit in sliced_fruits:
            mes_fruits.remove(fruit)
            print(f"[J2 SOURIS] Fruit {fruit.type} slicé dans la zone DROITE!")  # Debug
        
        # Reset
        slicing = False
        slice_points = []

def line_intersects_fruit(points, fruit):
    """
    Vérifie si la ligne (liste de points) passe près du fruit
    Amélioration : vérifie aussi les segments entre les points
    """
    if len(points) < 2:
        return False
    
    # Méthode 1 : vérifier chaque point de la traînée
    for point in points:
        dx = point[0] - fruit.x
        dy = point[1] - fruit.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < fruit.radius + 20:  # Marge de collision
            return True
    
    # Méthode 2 : vérifier les segments entre les points (plus précis)
    for i in range(len(points) - 1):
        if segment_intersects_circle(points[i], points[i+1], fruit):
            return True
    
    return False

def segment_intersects_circle(p1, p2, fruit):
    """
    Vérifie si un segment de ligne intersecte un cercle (le fruit)
    p1, p2 : points du segment (x, y)
    fruit : objet Fruit avec x, y, radius
    """
    # Vecteur du segment
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    
    # Vecteur de p1 au centre du cercle
    fx = fruit.x - p1[0]
    fy = fruit.y - p1[1]
    
    # Longueur du segment au carré
    segment_length_sq = dx * dx + dy * dy
    
    if segment_length_sq == 0:
        # Le segment est un point
        distance = math.sqrt(fx * fx + fy * fy)
        return distance < fruit.radius + 20
    
    # Projection du point du fruit sur le segment (paramètre t)
    t = max(0, min(1, (fx * dx + fy * dy) / segment_length_sq))
    
    # Point le plus proche sur le segment
    closest_x = p1[0] + t * dx
    closest_y = p1[1] + t * dy
    
    # Distance entre ce point et le centre du fruit
    dist_x = fruit.x - closest_x
    dist_y = fruit.y - closest_y
    distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
    
    return distance < fruit.radius + 20

def draw_slice(surface):
    """Dessine la traînée en cours (ligne rouge épaisse)"""
    if len(slice_points) > 1:
        pygame.draw.lines(surface, (255, 0, 0), False, slice_points, 5)

def handle_keyboard_inputs(mes_fruits, screen_width, screen_height, key):
    """
    Gestion du slicing par zones clavier (ZSDE)
    ZONE JOUEUR 1 : Fonctionne UNIQUEMENT sur la moitié GAUCHE de l'écran
    
    Les 4 quadrants sont dans la MOITIÉ GAUCHE :
    Z : Haut-gauche
    S : Bas-gauche  
    D : Bas-droite (de la moitié gauche)
    E : Haut-droite (de la moitié gauche)
    """
    # ==========================================
    # CALCUL DU MILIEU DE L'ÉCRAN
    # ==========================================
    milieu_x = screen_width // 2
    
    # ==========================================
    # ZONES LIMITÉES À LA MOITIÉ GAUCHE
    # ==========================================
    zones = {
        pygame.K_z: (0, 0, milieu_x // 2, screen_height // 2),                     # Haut-gauche (quart supérieur gauche)
        pygame.K_s: (0, screen_height // 2, milieu_x // 2, screen_height),         # Bas-gauche (quart inférieur gauche)
        pygame.K_d: (milieu_x // 2, screen_height // 2, milieu_x, screen_height),  # Bas-droite de la zone gauche
        pygame.K_e: (milieu_x // 2, 0, milieu_x, screen_height // 2)               # Haut-droite de la zone gauche
    }
    
    if key in zones:
        zone = zones[key]
        sliced = 0
        for fruit in mes_fruits[:]:  # Copie pour éviter erreurs lors de suppression
            # ==========================================
            # VÉRIFICATION : Fruit dans la zone spécifiée ET dans la moitié GAUCHE
            # ==========================================
            if zone[0] <= fruit.x <= zone[2] and zone[1] <= fruit.y <= zone[3]:
                # Double vérification : le fruit est bien dans la moitié gauche
                if fruit.x < milieu_x:
                    mes_fruits.remove(fruit)
                    sliced += 1
        
        if sliced > 0:
            print(f"[J1 CLAVIER] {sliced} fruit(s) slicé(s) dans la zone GAUCHE!")  # Debug

def save_scores(score_j1, score_j2):
    """Sauvegarde les scores dans un fichier JSON (prévu pour le mode 2 joueurs)"""
    data = {'joueur1': score_j1, 'joueur2': score_j2}
    with open('scores.json', 'w') as f:
        json.dump(data, f)