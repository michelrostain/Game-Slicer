import pygame

liste_fruits=["poire", "pomme", "banane", "orange"]

images = {}

def load_assets():
    images["pomme"] = pygame.image.load("Assets/Images/pomme.jpg").convert_alpha()
