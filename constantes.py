import pygame

liste_fruits=["poire", "pomme", "banane", "orange"]

images = {}

def load_assets():
    """
    Docstring for load_assets
    
    :param None: Charge les images des fruits dans le dictionnaire images
    """
    
    try:
        images["pomme"] = pygame.image.load("Assets/Images/pomme.jpg").convert_alpha()
        print("✓ Image pomme chargée")
    except pygame.error as e:
        print(f"✗ Erreur chargement pomme.jpg : {e}")
        images["pomme"] = None
        
# Configuration du jeu (pour le futur menu)
CONFIG = {
    "nb_joueurs": 1,  # 1 ou 2 joueurs
    "difficulte": "normal",  # facile, normal, difficile
    "duree_partie": 60,  # en secondes
    "spawn_bombes": True,  # Activer/désactiver les bombes
    "spawn_bonus": True   # Activer/désactiver les bonus
}
