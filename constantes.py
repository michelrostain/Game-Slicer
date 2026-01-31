import pygame

liste_fruits = ["poire", "pomme", "banane", "orange"]

images = {}  # Dict vide, rempli dans load_assets()

def load_assets():
    """
    Charge les images des fruits dans le dictionnaire images
    """
    try:
        images["poire"] = {
            "up": pygame.image.load("Assets/Images/Fruits/angry_pear.png").convert_alpha(),
            "down": pygame.image.load("Assets/Images/Fruits/scared_pear.png").convert_alpha(),
            "cut": pygame.image.load("Assets/Images/Fruits/cut_pear.png").convert_alpha(),
        }
        print("✓ Images poires chargées")

        images["pomme"] = {
            "up": pygame.image.load("Assets/Images/Fruits/angry_apple.png").convert_alpha(),
            "down": pygame.image.load("Assets/Images/Fruits/scared_apple.png").convert_alpha(),
            "cut": pygame.image.load("Assets/Images/Fruits/cut_apple.png").convert_alpha(),
        }
        print("✓ Images pommes chargées")

        images["banane"] = {
            "up": pygame.image.load("Assets/Images/Fruits/angry_banana.png").convert_alpha(),
            "down": pygame.image.load("Assets/Images/Fruits/scared_banana.png").convert_alpha(),
            "cut": pygame.image.load("Assets/Images/Fruits/cut_banana.png").convert_alpha(),
        }
        print("✓ Images bananes chargées")

        images["orange"] = {
            "up": pygame.image.load("Assets/Images/Fruits/angry_orange.png").convert_alpha(),
            "down": pygame.image.load("Assets/Images/Fruits/scared_orange.png").convert_alpha(),
            "cut": pygame.image.load("Assets/Images/Fruits/cut_orange.png").convert_alpha(),
        }
        print("✓ Images oranges chargées")

    except pygame.error as e:
        print(f"✗ Erreur chargement images : {e}")
        # Fallback
        for fruit in liste_fruits:
            images[fruit] = None

# Configuration du jeu (pour le futur menu)
CONFIG = {
    "nb_joueurs": 1,  # 1 ou 2 joueurs
    "difficulte": "normal",  # facile, normal, difficile
    "duree_partie": 60,  # en secondes
    "spawn_bombes": True,  # Activer/désactiver les bombes
    "spawn_bonus": True   # Activer/désactiver les bonus
}