import pygame, random
from constantes import images

class Fruit:
    def __init__(self, type_de_fruit, largeur, hauteur, zone_joueur=None):
        self.type=type_de_fruit
        
        # Association de l'image aux types de fruits sélectionnés
        images_trouvees = images.get(self.type)
        
        if images_trouvees is not None:
            # Redimensionnement de l'image
            self.image=pygame.transform.scale(images_trouvees, (100, 100))
        else:
            self.image=None

        # Rayon du fruit pour les collisions
        self.radius = 50
        
        # ============================================
        # GÉNÉRATION PAR ZONE (JOUEUR 1 ou 2)
        # ============================================
        milieu_x = largeur // 2
        
        if zone_joueur == 1:
            # Zone GAUCHE (Joueur 1) - entre 100 et le milieu
            self.x = random.randint(100, milieu_x - 100)
        elif zone_joueur == 2:
            # Zone DROITE (Joueur 2) - entre le milieu et la largeur
            self.x = random.randint(milieu_x + 100, largeur - 100)
        else:
            # Par défaut : n'importe où (mode 1 joueur)
            self.x = random.randint(100, largeur - 100)
        
        # Position de départ (en bas de l'écran)
        self.y = hauteur
        
        # ============================================
        # REBOND LIMITÉ À LA ZONE DU JOUEUR
        # ============================================
        self.zone_joueur = zone_joueur
        self.milieu_x = milieu_x
        
        # Physique du mouvement
        self.speed_x = random.uniform(-10, 10)  # Vitesse horizontale
        self.speed_y = random.uniform(-20, -10)  # Vitesse verticale (vers le haut)
        self.gravity = 0.4
        
        # Couleur par défaut si pas d'image
        self.color = self.get_color_for_fruit(type_de_fruit)
        
    def get_color_for_fruit(self, type_de_fruit):
        """
        Docstring for get_color_for_fruit
        
        :param self: Instance de la classe Fruit
        :param type_de_fruit: Type de fruit (str)
        :return: Couleur RGB associée au type de fruit
        """
        colors = {
            "pomme": (255, 0, 0),    # Rouge
            "poire": (144, 238, 144), # Vert clair
            "banane": (255, 255, 0),  # Jaune
            "orange": (255, 165, 0)   # Orange
        }
        return colors.get(type_de_fruit, (255, 255, 255))  # Blanc par défaut


    def update(self, largeur_ecran):
        """
        Docstring for update
        
        :param self: Instance de la classe Fruit
        :param largeur_ecran: Largeur de l'écran (int)
        :return: None
        """
        
        # On applique la gravité à la vitesse verticale
        self.speed_y += self.gravity
        
        # On met à jour la position avec les vitesses
        self.x += self.speed_x
        self.y += self.speed_y

        # ============================================
        # REBONDS LIMITÉS PAR ZONE
        # ============================================
        if self.zone_joueur == 1:
            # Zone GAUCHE (Joueur 1) - rebondit entre 0 et milieu_x
            if self.x - self.radius < 0:
                self.x = self.radius
                self.speed_x *= -1
            
            if self.x + self.radius > self.milieu_x:
                self.x = self.milieu_x - self.radius
                self.speed_x *= -1
                
        elif self.zone_joueur == 2:
            # Zone DROITE (Joueur 2) - rebondit entre milieu_x et largeur_ecran
            if self.x - self.radius < self.milieu_x:
                self.x = self.milieu_x + self.radius
                self.speed_x *= -1
            
            if self.x + self.radius > largeur_ecran:
                self.x = largeur_ecran - self.radius
                self.speed_x *= -1
        else:
            # Mode 1 joueur - rebondit sur toute la largeur
            if self.x - self.radius < 0:
                self.x = self.radius
                self.speed_x *= -1
            
            if self.x + self.radius > largeur_ecran:
                self.x = largeur_ecran - self.radius
                self.speed_x *= -1

    def draw(self, surface):
        """
        Docstring for draw
        
        :param self: Instance de la classe Fruit
        :param surface: Surface Pygame sur laquelle dessiner
        """
        
        # On importe l'image
        if self.image:
            # Centrage de l'image (100x100) sur la position (x, y)
            surface.blit(self.image, (int(self.x) -50, int(self.y) -50)) # les "-25" servent à ventrer la photo au centre. Notre rescale étant de 50 par 50, on a donc le centre qui est à 25.
        else :
        # Si image pas trouvée
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        


class bombe:
    def __init__(self, largeur, hauteur):
        # 1. Apparence
        self.radius = 40
        self.color = (0, 0, 0)  # Noir

        # Position et physique similaires aux fruits
        self.x = random.randint(100, largeur - 100)
        self.y = hauteur
        self.speed_x = random.uniform(-8, 8)
        self.speed_y = random.uniform(-18, -12)
        self.gravity = 0.4
        
    def update(self, largeur_ecran):
        """Met à jour la position de la bombe"""
        self.speed_y += self.gravity
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Rebonds
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -1
        
        if self.x + self.radius > largeur_ecran:
            self.x = largeur_ecran - self.radius
            self.speed_x *= -1
    
    def draw(self, surface):
        """Affiche la bombe"""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Ajout d'une mèche (ligne blanche)
        pygame.draw.line(surface, (255, 255, 255), 
                        (int(self.x), int(self.y) - self.radius),
                        (int(self.x), int(self.y) - self.radius - 20), 3)

class ice:
    """Classe pour les bonus ice/freeze (à implémenter)"""
    def __init__(self, largeur, hauteur):
        self.radius = 40
        self.color = (173, 216, 230)  # Bleu clair
        
        self.x = random.randint(100, largeur - 100)
        self.y = hauteur
        self.speed_x = random.uniform(-8, 8)
        self.speed_y = random.uniform(-18, -12)
        self.gravity = 0.4
    
    def update(self, largeur_ecran):
        """Met à jour la position du bonus ice"""
        self.speed_y += self.gravity
        self.x += self.speed_x
        self.y += self.speed_y
        
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -1
        
        if self.x + self.radius > largeur_ecran:
            self.x = largeur_ecran - self.radius
            self.speed_x *= -1
    
    def draw(self, surface):
        """Affiche le bonus ice"""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
