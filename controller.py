import pygame
import json

def handle_mouse_inputs(mes_fruits, mouse_pos):
    # Détecte collision souris-fruits
    for fruit in mes_fruits[:]:  # Copie pour éviter erreurs lors de suppression
        dx = mouse_pos[0] - fruit.x
        dy = mouse_pos[1] - fruit.y
        distance = (dx**2 + dy**2)**0.5
        if distance < fruit.radius:
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