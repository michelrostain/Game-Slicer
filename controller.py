import pygame
import json
import math

# Variables pour le slicing souris
slicing = False  # Si on est en train de slicer
slice_points = []  # Liste des points de la traînée (x, y)

def start_slice(mouse_pos):
    global slicing, slice_points
    slicing = True
    slice_points = [mouse_pos]  # Commence avec le point initial

def update_slice(mouse_pos):
    global slice_points
    if slicing:
        slice_points.append(mouse_pos)  # Ajoute le point actuel

def end_slice(mes_fruits):
    global slicing, slice_points
    if slicing:
        # Vérifie les collisions avec la ligne tracée
        sliced_fruits = []
        for fruit in mes_fruits:
            if line_intersects_fruit(slice_points, fruit):
                sliced_fruits.append(fruit)
        # Supprime les fruits slicés
        for fruit in sliced_fruits:
            mes_fruits.remove(fruit)
        # Reset
        slicing = False
        slice_points = []

def line_intersects_fruit(points, fruit):
    # Vérifie si la ligne (liste de points) passe près du fruit (collision approximative)
    for point in points:
        dx = point[0] - fruit.x
        dy = point[1] - fruit.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < fruit.radius + 30:  # +30 pour marge (ajuste si besoin)
            return True
    return False

def draw_slice(surface):
    # Dessine la traînée en cours (ligne rouge)
    if len(slice_points) > 1:
        pygame.draw.lines(surface, (255, 0, 0), False, slice_points, 5)  # Ligne rouge épaisse

def handle_mouse_inputs(mes_fruits, mouse_pos):
    # Détecte collision souris-fruits
    for fruit in mes_fruits[:]:  # Copie pour éviter erreurs lors de suppression
        dx = mouse_pos[0] - fruit.x
        dy = mouse_pos[1] - fruit.y
        distance = (dx**2 + dy**2)**0.5
        if distance < fruit.radius + 30:
            mes_fruits.remove(fruit)  # "Slice" le fruit (à améliorer avec score/effets)

def handle_keyboard_inputs(mes_fruits, screen_width, screen_height, key):
    # Définit 4 zones (quadrants)
    zones = {
        pygame.K_z: (0, 0, screen_width//2, screen_height//2),                          # Haut-gauche
        pygame.K_s: (0, screen_height//2, screen_width//2, screen_height),               # Bas-gauche
        pygame.K_d: (screen_width//2, screen_height//2, screen_width, screen_height),    # Bas-droite
        pygame.K_r: (screen_width//2, 0, screen_width, screen_height//2)               # Haut-droite
    }
    if key in zones:
        zone = zones[key]
        for fruit in mes_fruits[:]:
            if zone[0] <= fruit.x <= zone[2] and zone[1] <= fruit.y <= zone[3]:
                mes_fruits.remove(fruit)
            
def save_scores(score_j1, score_j2):
    data = {'joueur1': score_j1, 'joueur2': score_j2}
    with open('scores.json', 'w') as f:
        json.dump(data, f)