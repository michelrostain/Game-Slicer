import pygame, random
from constantes import images

# Dans objets.py

class Fruit:
    def __init__(self, type_de_fruit, largeur, hauteur, zone_joueur=None):
        self.type = type_de_fruit
        self.sliced = False
        self.radius = 45 # Légèrement réduit pour mieux coller aux fruits fins
        
        # --- GESTION INTELLIGENTE DES IMAGES ---
        raw_image = images.get(self.type)
        self.images_set = None 
        
        # Hauteur qu'on veut pour tous les fruits (en pixels)
        HAUTEUR_CIBLE = 110 

        if isinstance(raw_image, dict):
            # C'est une POIRE (Dictionnaire d'images)
            self.images_set = {}
            for key, img_orig in raw_image.items():
                # 1. On calcule le ratio (Largeur / Hauteur)
                ratio = img_orig.get_width() / img_orig.get_height()
                # 2. On calcule la nouvelle largeur pour garder les proportions
                nouvelle_largeur = int(HAUTEUR_CIBLE * ratio)
                # 3. On redimensionne proprement (smoothscale est plus joli que scale)
                self.images_set[key] = pygame.transform.smoothscale(img_orig, (nouvelle_largeur, HAUTEUR_CIBLE))
            
            self.image = self.images_set["up"]

        elif raw_image is not None:
            # C'est un FRUIT SIMPLE
            ratio = raw_image.get_width() / raw_image.get_height()
            nouvelle_largeur = int(HAUTEUR_CIBLE * ratio)
            self.image = pygame.transform.smoothscale(raw_image, (nouvelle_largeur, HAUTEUR_CIBLE))
        else:
            self.image = None

        # --- LE RESTE EST INCHANGÉ ---
        milieu_x = largeur // 2
        if zone_joueur == 1: self.x = random.randint(100, milieu_x - 100)
        elif zone_joueur == 2: self.x = random.randint(milieu_x + 100, largeur - 100)
        else: self.x = random.randint(100, largeur - 100)
        
        self.y = hauteur
        self.speed_x = random.uniform(-10, 10)
        self.speed_y = random.uniform(-20, -10)
        self.gravity = 0.4
        
        self.color = (255, 0, 0)
        if self.type == "banane": self.color = (255, 255, 0)
        elif self.type == "orange": self.color = (255, 165, 0)

    # ... (Garde les méthodes update, couper et draw comme avant) ...
    # Si tu as besoin, je peux te redonner tout le fichier, 
    # mais seule la partie __init__ ci-dessus a changé.
    
    def update(self, largeur_ecran, speed_factor=1):
        # ... (copier le code précédent) ...
        self.speed_y += self.gravity * speed_factor
        self.x += self.speed_x * speed_factor
        self.y += self.speed_y * speed_factor

        if self.images_set and not self.sliced:
            if self.speed_y < 0: self.image = self.images_set["up"]
            else: self.image = self.images_set["down"]

        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -1
        if self.x + self.radius > largeur_ecran:
            self.x = largeur_ecran - self.radius
            self.speed_x *= -1

    def couper(self):
        self.sliced = True
        if self.images_set:
            self.image = self.images_set["cut"]
            self.speed_y = -5

    def draw(self, screen):
        if self.image:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    def couper(self):
        """Appelé quand le fruit est tranché"""
        self.sliced = True
        if self.images_set:
            self.image = self.images_set["cut"]
            self.speed_y = -5 # Petit saut visuel quand coupé

    def draw(self, screen):
        if self.image:
            # On centre l'image sur la position x,y
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Glacon:
    def __init__(self, largeur, hauteur):
        self.type = "glacon"
        self.sliced = False
        self.images_set = None
        
        self.radius = 40
        self.color = (173, 216, 230)  # Bleu clair
        
        self.x = random.randint(100, largeur - 100)
        self.y = hauteur
        self.speed_x = random.uniform(-8, 8)
        self.speed_y = random.uniform(-18, -12)
        self.gravity = 0.4
    
    def update(self, largeur_ecran, speed_factor=1):
        """Met à jour le glaçon"""
        # Le glaçon est aussi affecté par le speed_factor (il peut s'auto-geler si on veut)
        self.speed_y += self.gravity * speed_factor
        self.x += self.speed_x * speed_factor
        self.y += self.speed_y * speed_factor
        
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -1
        
        if self.x + self.radius > largeur_ecran:
            self.x = largeur_ecran - self.radius
            self.speed_x *= -1
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Effet de reflet blanc
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x - 10), int(self.y - 10)), 10)